from tqdm import tqdm

n_max = 10


def get_instance_details(x):

    projects = x.select('xnat:projectData').all().data
    params = {'columns': 'ID,project,handedness,age,gender'}
    j = x.get('/data/subjects', params=params).json()
    subjects = j['ResultSet']['Result']

    experiments = x.array.experiments(columns=['subject_ID', 'date'],
                                      experiment_type='').data

    columns = ['xnat:imageScanData/quality',  'xnat:imageScanData/type']
    scans = x.array.scans(columns=columns).data

    data = {}
    data['projects'] = projects
    data['subjects'] = subjects
    data['experiments'] = experiments
    data['scans'] = scans

    return data


def get_resources(x):

    experiments = x.array.experiments(columns=['subject_ID', 'date'],
                                      experiment_type='').data
    resources = []
    resources_bbrc = []

    # For each experiments fetch all the resources associated with it
    for exp in tqdm(experiments[:n_max]):
        # -------------------- RESOURCES--------------------------------#
        res = x._get_json('{}/{}'.format(exp['URI'], 'resources'))
        if len(res) == 0:
            resources.append([exp['project'], exp['ID'], 'No Data', 'No Data'])
        else:
            for r in res:
                row = [exp['project'], exp['ID'],
                       r['xnat_abstractresource_id'], r['label']]
                resources.append(row)

        # -------------------- BBRC RESOURCES--------------------------------#
        # BBRC_VALIDATOR
        e = x.select.experiment(exp['ID'])
        bbrc_validator = e.resource('BBRC_VALIDATOR')
        if bbrc_validator.exists():
            row = [exp['project'], exp['ID'], True,
                   tests_resource(bbrc_validator, 'ArchivingValidator')]
            resources_bbrc.append(row)
        else:
            resources_bbrc.append([exp['project'], exp['ID'], False, 0])

    return resources, resources_bbrc


def tests_resource(res, name):
    import json
    try:
        j = [e for e in list(res.files('{}*.json'.format(name)))][0]
        j = json.loads(res._intf.get(j._uri).text)
        return j
    except IndexError:
        return 0


def longitudinal_data(details, resources):
    # Get current time
    from datetime import datetime

    now = datetime.now()
    dt = now.strftime("%d/%m/%Y")

    res = {}
    eobjects = ['Projects', 'Subjects', 'Experiments', 'Scans']
    names = ['projects', 'subjects', 'experiments', 'scans']

    for each in eobjects:
        res[each] = {}

    for eobj, n in zip(eobjects, names):
        res[eobj]['count'] = {dt: len(details[n])}

    for n in names:
        for p in details[n]:
            res[eobj].setdefault('list', {})
            k = 'ID' if n != 'projects' else 'id'
            res[eobj]['list'].setdefault(dt, []).append(p[k])

    # Resources
    res['Resources'] = {}
    for e_proj, e_id, r_id, r_label in resources:
        if r_id:
            a = str(e_id) + '  ' + str(r_id)
            res['Resources'].setdefault('list', {})
            res['Resources']['list'].setdefault(dt, []).append(a)

    res['Resources']['count'] = {dt: len(res['Resources']['list'][dt])}

    return res
