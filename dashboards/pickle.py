import pickle
import os.path as op
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

    # For each experiments fetch all the resources associated with it
    for exp in tqdm(experiments[:n_max]):

        res = x._get_json('{}/{}'.format(exp['URI'], 'resources'))

        e = x.select.experiment(exp['ID'])
        bbrc_validator = e.resource('BBRC_VALIDATOR')
        insert_date = exp['insert_date'].split(' ')[0]

        if len(res) == 0:
            row = [exp['project'], exp['ID'], 'No Data', 'No Data']
        else:
            for r in res:
                row = [exp['project'], exp['ID'],
                       r['xnat_abstractresource_id'], r['label']]

        tv = get_tests(bbrc_validator, 'ArchivingValidator')

        row.extend([tv[0], tv[1], insert_date])

        resources.append(row)

        # # -------------------- BBRC RESOURCES--------------------------------#
        # # BBRC_VALIDATOR
        # e = x.select.experiment(exp['ID'])
        # bbrc_validator = e.resource('BBRC_VALIDATOR')
        # insert_date = exp['insert_date'].split(' ')[0]
        # row = [exp['project'], exp['ID'], tv[0], tv[1], insert_date]
        # resources_bbrc.append(row)

    return resources


def get_tests(resource, validator_name):

    import json
    val = []
    av = 0
    validators = [e for e in list(resource.files('*.json'))]
    if validators:
        for v in validators:
            if validator_name in str(v):
                av = json.loads(resource._intf.get(v._uri).text)
            v = ((str(v).split('>')[1]).split('_')[0]).strip(' ')
            val.append(v)
        return av, val
    else:
        return av, val


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


def save(x, fp):

    p = {}

    # Raise Exception if file exists with different server name
    if op.isfile(fp) and op.getsize(fp) > 0:

        p = pickle.load(open(fp, 'rb'))
        if 'server' in p and x._server != p['server']:
            msg = 'Pickle server mismatch %s %s %s'\
                  % (fp, p['server'], x._server)
            raise Exception(msg)

        # Backup pickle
        print('Prior pickle found at %s. Backing up at %s.bak.' % (fp, fp))
        pickle.dump(p, open('%s.bak' % fp, 'wb'))

    details = get_instance_details(x)

    resources = get_resources(x)

    res = ['FREESURFER6', 'FREESURFER6_HIRES', 'ASHS', 'BAMOS',
           'SPM12_SEGMENT']
    long_data = {}

    for resource_name in res:
        dt, n_res = resource_monitor(x, resources, resource_name)

        if 'longitudinal_data' in p.keys():
            long_data = p['longitudinal_data']
            if resource_name not in long_data:
                long_data[resource_name] = {dt: n_res}
            long_data[resource_name][dt] = n_res
        else:
            long_data[resource_name] = {dt: n_res}

    bbrc_resources = []
    resources2 = []
    for e in resources:
        resources2.append(e[:4])
        bbrc_resources.append([e[0], e[1], e[-3], e[-2], e[-1]])

    resources2.extend(bbrc_resources)

    d = {'server': x._server,
         'verify': x._verify,
         'info': details,
         'resources': resources2,
         #'extra_resources': bbrc_resources,
         'longitudinal_data': long_data}
    p.update(d)

    # Save all the data to pickle
    pickle.dump(p, open(fp, 'wb'))
    print('Pickle file successfully saved at', fp)


def load(server):
    """Opens pickle file to be used the the dashboard
    controller.

    Args:
        server (str): URL of the server where user is
            is registered.

    Returns:
        dict/None: If server details are mistaching it returns
        None else returns the details from pickle as a dict.
    """



    return user_data
