from pyxnat_connection import get_info


class projectGenerator:

    data = {}

    def __init__(self, user, password, server):
        self.data = get_info.GetInfo(user,
                                     password,
                                     server).get_project_list()

    def project_list(self):

        # Returns a the names of project based in a 2dArray
        # To be processed by frontend
        length_check = 0
        array_2d = []
        array_1d = []
        counter = 0

        list_data = self.data
        if(type(list_data) == int):
            return list_data

        for data in list_data:
            array_1d.append(data)
            counter = counter + 1
            if(counter == 4 or length_check == len(list_data)-1):
                counter = 0
                array_2d.append(array_1d)
                array_1d = []

            length_check = length_check+1

        return array_2d
