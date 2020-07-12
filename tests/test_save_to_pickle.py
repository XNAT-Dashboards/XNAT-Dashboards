from save_endpoint import save_to_pickle
import os
import pickle
from pymongo import MongoClient


def test_save_data_and_user():

    username = 'testUser'
    password = 'testPassword'
    server = 'https://central.xnat.org'
    ssl = False

    saving_object = save_to_pickle.SaveToPk(
        username, password, server, ssl)
    saving_object.save_data()

    with open('pickles/users_data/testUser.pickle', 'rb') as handle:
        user_data = pickle.load(handle)

    assert type(user_data['info']) == dict

    # Save user

    saving_object.save_user(username, password, server, ssl)

    with open('pickles/users/testUser.pickle', 'rb') as handle:
        existing_user = pickle.load(handle)

    assert existing_user['username'] == 'testUser'
    assert existing_user['password'] == 'testPassword'
    assert existing_user['server'] == 'https://central.xnat.org'
    assert existing_user['ssl'] is False
