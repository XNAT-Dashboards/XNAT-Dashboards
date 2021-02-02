import pickle
import os.path as op
from dashboards import data_fetcher

def save(x, fp):

    p = {}

    # Raise Exception if file exists with different server name
    if op.isfile(fp) and op.getsize(fp) > 0:
        with open(fp, 'rb') as handle:
            p = pickle.load(handle)

            if 'server' in p and x._server != p['server']:
                    msg = "Server URL present in pickle is "\
                        "different form the provided server URL"
                    raise Exception(msg)

    # Copy of the last valid pickle file
    backup = p

    #try:
    details = data_fetcher.get_instance_details(x)

    resources, bbrc_resources = data_fetcher.get_resources(x)

    res = ['FREESURFER6', 'FREESURFER6_HIRES', 'ASHS', 'BAMOS']
    long_data = {}

    for resource_name in res:
        dt, n_res = data_fetcher.resource_monitor(x, resources, resource_name)
        try:
            long_data = p['longitudinal_data']
            if resource_name not in long_data:
                long_data[resource_name] = {dt: n_res}
            long_data[resource_name][dt] = n_res
        except:
            long_data[resource_name] = {dt: n_res}

    d = {'server': x._server,
         'verify': x._verify,
         'info': details,
         'resources': resources,
         'extra_resources': bbrc_resources,
         'longitudinal_data': long_data}
    p.update(d)

    # Save all the data to pickle
    with open(fp, 'wb') as h:
        pickle.dump(p, h, protocol=pickle.HIGHEST_PROTOCOL)

    print("Pickle file successfully saved at", fp)
    # except:
    #     # Save backup file
    #     with open(fp, 'wb') as h:
    #         pickle.dump(backup, h, protocol=pickle.HIGHEST_PROTOCOL)
    #
    #     print("Backup file successfully saved at", fp)