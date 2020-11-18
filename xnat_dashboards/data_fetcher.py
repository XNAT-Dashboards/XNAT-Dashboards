import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")

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

    # For each experiments fetch all the resources associated with it
    for e in tqdm(list(experiments)[:n_max]):

        res = x.select.experiments(e['ID']).resources()
        res = list(res)

        if len(res) == 0:
            row = [e['project'], e['ID'], None, None]
            resources.append(row)
        else:
            for r in res:
                row = [e['project'], e['ID'], r.id(), r.label()]
                resources.append(row)

    return resources


def get_resources_bbrc(x):

    import json
    experiments = x.array.experiments(columns=['subject_ID', 'date'],
                                      experiment_type='').data
    resources = []

    for exp in tqdm(list(experiments)[:n_max]):

        e = x.select.experiment(exp['ID'])
        v = e.resource('BBRC_VALIDATOR')

        try:
            name = 'ArchivingValidator'
            j = [e for e in list(v.files('{}*.json'.format(name)))][0]
            j = json.loads(v._intf.get(j._uri).text)

        except IndexError as exc:
            print(exc, exp['ID'])
            j = 0

        row = [exp['project'], exp['ID'], v.exists(), j]
        resources.append(row)

    return resources


def longitudinal_data(details, resources):
    # Get current time
    from datetime import datetime

    now = datetime.now()
    dt = now.strftime("%d/%m/%Y")

    res = {}
    eobjects = ['Project', 'Subjects', 'Experiments', 'Scans']
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
