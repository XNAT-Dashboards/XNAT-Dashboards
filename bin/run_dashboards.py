#!/usr/bin/env python

def create_args():
    import argparse
    from argparse import RawTextHelpFormatter

    desc = 'Run the webapp given a previously generated pickle file (yielded '\
           'by download_data.py) and a configuration file (JSON file describing '\
           'the different plots and access rights)'

    ap = argparse.ArgumentParser(description=desc,
                                 formatter_class=RawTextHelpFormatter)
    ap.add_argument('-p', '--pickle', help='Path to pickle', required=True)
    ap.add_argument('-c', '--config', help='Path to configuration file',
                    required=True)
    ap.add_argument('-P', '--port', help='Port number', default=5000)
    ap.add_argument('-u', '--url', help='URL for the server', default='0.0.0.0')
    ap.add_argument('--debug', help='Debug mode', action='store_true',
                    default=False)
    return ap


if __name__ == "__main__":
    parser = create_args()
    args = parser.parse_args()

    from dashboards import config
    from dashboards.app import app
    import os.path as op

    config.DASHBOARD_CONFIG_PATH = op.abspath(args.config)
    config.PICKLE_PATH = op.abspath(args.pickle)
    app.run(host=args.url, port=args.port, debug=args.debug)
