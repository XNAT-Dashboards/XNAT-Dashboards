import os
import os.path as op
import logging as log

n_max = 50 if os.environ.get('CI_TEST', None) else None


def get_projects(x):
    projects = x.select('xnat:projectData').all().data
    return projects


def get_subjects(x):
    params = {'columns': 'ID,project,handedness,age,gender'}
    j = x.get('/data/subjects', params=params).json()
    subjects = j['ResultSet']['Result']
    return subjects


def get_experiments(x):
    experiments = x.array.experiments(columns=['subject_ID', 'date']).data
    return experiments


def get_scans(x):
    columns = ['xnat:imageScanData/quality', 'xnat:imageScanData/type']
    scans = x.array.scans(columns=columns).data
    return scans


def get_resources(x):
    from tqdm import tqdm

    resources = []

    experiments = x.array.experiments(columns=['ID', 'project']).data
    # For each experiments fetch all the resources associated with it
    for exp in tqdm(experiments[:n_max]):
        j = x.get('{}/{}'.format(exp['URI'], 'resources')).json()
        exp_res = j['ResultSet']['Result']

        if exp_res:
            resources.extend([[exp['project'], exp['ID'],
                               r['xnat_abstractresource_id'],
                               r['label']] for r in exp_res])
        else:
            resources.append([exp['project'], exp['ID'],
                              'No Data', 'No Data'])
    return resources


def get_bbrc_resources(x):
    from tqdm import tqdm

    resources_bbrc = []
    validator = 'ArchivingValidator'

    cols = ['subject_ID', 'date', 'insert_date']
    experiments = x.array.experiments(columns=cols).data
    for exp in tqdm(experiments[:n_max]):
        insert_date = exp['insert_date'].split(' ')[0]

        r = x.select.experiment(exp['ID']).resource('BBRC_VALIDATOR')
        val_results, val_list = get_bbrc_tests(r, validator)

        row = [exp['project'], exp['ID'], val_results, val_list, insert_date]
        resources_bbrc.append(row)

    return resources_bbrc


def get_bbrc_tests(resource, validator_name):

    import json
    val_list = []
    val_result = 'No Data'
    validators = [e for e in list(resource.files('*.json'))]
    if validators:
        for v in validators:
            if validator_name in str(v):
                val_result = json.loads(resource._intf.get(v._uri).text)
            val_name = ((str(v).split('>')[1]).split('_')[0]).strip(' ')
            val_list.append(val_name)

    return val_result, val_list


def update_longitudinal_data(pickle_data, resources):
    from datetime import datetime

    # Get current time
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y")

    # Count total number of resources
    import pandas as pd
    columns = ['project', 'eid', 'xnat_abstractresource_id', 'label']
    df = pd.DataFrame(resources, columns=columns)[['project', 'label']]
    n_res = df.groupby('label').count().to_dict()['project']

    # Update longitudinal resource data with additional timepoint
    long_data = pickle_data.get('longitudinal_data', {})
    for resource_name in list(n_res.keys()):
        long_data.setdefault(resource_name, {})
        long_data[resource_name][dt] = n_res[resource_name]

    return long_data


def get_data(x):
    """Fetch XNAT data entities as a dictionary."""

    data = dict()
    data['server'] = x._server
    data['verify'] = x._verify
    data['projects'] = get_projects(x)
    data['subjects'] = get_subjects(x)
    data['experiments'] = get_experiments(x)
    data['scans'] = get_scans(x)
    data['resources'] = get_resources(x)
    data['bbrc_resources'] = get_bbrc_resources(x)
    return data


def save(x, fp):
    import pickle

    p = {}

    # Raise Exception if file exists with different server name
    if op.isfile(fp) and op.getsize(fp) > 0:
        p = pickle.load(open(fp, 'rb'))
        if x._server != p.get('server'):
            msg = 'Pickle server mismatch %s %s %s'\
                  % (fp, p['server'], x._server)
            raise Exception(msg)

        # Backup pickle
        log.warning('Backing up at %s.bak.' % fp)
        pickle.dump(p, open('%s.bak' % fp, 'wb'))

    # Get XNAT data
    d = get_data(x)
    d['longitudinal_data'] = update_longitudinal_data(p, d['resources'])
    # TODO: fix this and keep resources/bbrc_resources separated
    d['resources'].extend(d['bbrc_resources'])
    p.update(d)

    # Save all the data to pickle
    pickle.dump(p, open(fp, 'wb'))
    log.info('Pickle file successfully saved at %s' % fp)
