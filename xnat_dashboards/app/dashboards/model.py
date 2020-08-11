import pickle
from xnat_dashboards import path_creator


def load_users_data_pk(server):

    try:
        with open(
                path_creator.get_pickle_path(), 'rb') as handle:
            user_data = pickle.load(handle)

        if user_data['server'] != server:
            return None
    except FileNotFoundError:
        return None

    return user_data
