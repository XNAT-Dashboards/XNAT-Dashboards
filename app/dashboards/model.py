import pickle


def load_users_data_pk(server):

    try:
        with open(
                'pickles/data/general.pickle', 'rb') as handle:
            user_data = pickle.load(handle)

        if user_data['server'] != server:
            return None
    except FileNotFoundError:
        return None

    return user_data
