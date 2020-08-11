from xnat_dashboards.save_endpoint import save_to_pickle


class DownloadData:

    def save(self, username, password, server, ssl):

        save_to_pickle.SaveToPk(username, password, server, ssl)
