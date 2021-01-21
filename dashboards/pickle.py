import pickle
import os.path as op
from dashboards import data_fetcher
import json

def save(x, fp):

    import pyxnat
    p = {}

    # Raise Exception if file exists with different server name
    if op.isfile(fp) and op.getsize(fp) > 0:
        with open(fp, 'rb') as handle:
            p = pickle.load(handle)

            if 'server' in p and x._server != p['server']:
                    msg = "Server URL present in pickle is "\
                        "different form the provided server URL"
                    raise Exception(msg)

    details = data_fetcher.get_instance_details(x)

    resources, bbrc_resources = data_fetcher.get_resources(x)

    res = ['FREESURFER6', 'FREESURFER6_HIRES', 'ASHS']
    for resource_name in res:
        dt, n_res = data_fetcher.resource_monitor(x, resource_name)
        long_data = longitudinal_data(dt, n_res, resource_name)

    d = {'server': x._server,
         'verify': x._verify,
         'info': details,
         'resources': resources,
         'extra_resources': bbrc_resources}
    p.update(d)

    # Save all the data to pickle
    with open(fp, 'wb') as h:
        pickle.dump(p, h, protocol=pickle.HIGHEST_PROTOCOL)

    print("Pickle file successfully saved at", fp)

def longitudinal_data(dt, n_res, resource_name):

    if not op.isfile('l_data.json'):
        with open('l_data.json', 'a') as outfile:
            l_data = {resource_name: {dt: n_res}}
            json.dump(l_data, outfile)
    else:
        with open('l_data.json', 'r+') as f:
            dic = json.load(f)
            if resource_name not in dic:
                dic[resource_name] = {dt: n_res}
            dic[resource_name][dt] = n_res
            with open('l_data.json', 'w') as f:
                json.dump(dic, f)

    with open('l_data.json', 'r') as f:
        long_data = json.load(f)

    return long_data