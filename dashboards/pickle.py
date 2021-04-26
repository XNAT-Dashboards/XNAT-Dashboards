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
    resources_bbrc = []

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

                # tv = get_tests(bbrc_validator, 'ArchivingValidator')
                # row.extend([tv[0], tv[1], insert_date])
                resources.append(row)
        tv = get_tests(bbrc_validator, 'ArchivingValidator')
        row = [exp['project'], exp['ID'], tv[0], tv[1], insert_date]
        resources_bbrc.append(row)
    return resources, resources_bbrc


def get_tests(resource, validator_name):

    import json
    val = []
    av = 'No Data'
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


def resource_monitor(resources):

    # Get current time
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y")

    # Count total number of resources
    import pandas as pd
    columns = ['project', 'eid', 'xnat_abstractresource_id', 'label']
    df = pd.DataFrame(resources, columns=columns)[['project', 'label']]
    n_res = df.groupby('label').count().to_dict()['project']

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

    resources, bbrc_resources = get_resources(x)

    # Monitors
    # res = ['FREESURFER6', 'FREESURFER6_HIRES', 'ASHS', 'BAMOS',
    #       'SPM12_SEGMENT']

    dt, n_res = resource_monitor(resources)
    long_data = p.get('longitudinal_data', {})
    for resource_name in list(n_res.keys()):
        long_data.setdefault(resource_name, {})
        long_data[resource_name][dt] = n_res[resource_name]

    # bbrc_resources = []
    # resources = []
    # for e in resources:
    #     resources2.append(e[:4])
    #     bbrc_resources.append([e[0], e[1], e[-3], e[-2], e[-1]])
    resources.extend(bbrc_resources)

    details = get_instance_details(x)

    d = {'server': x._server,
         'verify': x._verify,
         'projects': details['projects'],
         'subjects': details['subjects'],
         'experiments': details['experiments'],
         'scans': details['scans'],
         'resources': resources,
         #'extra_resources': bbrc_resources,
         'longitudinal_data': long_data}
    p.update(d)

    # Save all the data to pickle
    pickle.dump(p, open(fp, 'wb'))
    print('Pickle file successfully saved at', fp)
