from tqdm import tqdm
import os

n_max = 10 if os.environ.get('CI_TEST', None) else None


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
