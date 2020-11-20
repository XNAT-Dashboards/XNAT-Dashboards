import pickle
import os.path as op
from xnat_dashboards import data_fetcher


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

    d = {'server': x._server,
         'verify': x._verify,
         'info': details,
         'resources': resources,
         'extra_resources': bbrc_resources}
    p.update(d)

    long_data = data_fetcher.longitudinal_data(details, resources)
    p.setdefault('longitudinal_data', {}).update(long_data)

    # Save all the data to pickle
    with open(fp, 'wb') as h:
        pickle.dump(p, h, protocol=pickle.HIGHEST_PROTOCOL)

    print("Pickle file successfully saved at", fp)
