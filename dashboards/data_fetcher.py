from tqdm import tqdm
import os
from datetime import datetime

n_max = 50 if os.environ.get('CI_TEST', None) else None


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

    experiments = x.array.experiments(columns=['subject_ID', 'date', 'insert_date'],
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
        insert_date = exp['insert_date'].split(' ')[0]
        row = [exp['project'], exp['ID'],
               tests_resource(bbrc_validator, 'ArchivingValidator')[0],
               tests_resource(bbrc_validator, 'ArchivingValidator')[1], insert_date]
        resources_bbrc.append(row)

    return resources, resources_bbrc


def tests_resource(res, name):
    import json
    val = []
    AV = 0
    validators = [e for e in list(res.files('*.json'))]
    if validators:
        for v in validators:
            if name in str(v):
                AV = json.loads(res._intf.get(v._uri).text)
            v = ((str(v).split('>')[1]).split('_')[0]).strip(' ')
            val.append(v)
        return AV, val
    else:
        return AV, val


def resource_monitor(x, resources, resource_name):

    # Get current time
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y")

    # Count total number of resources
    n_res = 0
    for r in resources:
        label = r[3]
        if label == resource_name:
            n_res = n_res + 1

    return dt, n_res