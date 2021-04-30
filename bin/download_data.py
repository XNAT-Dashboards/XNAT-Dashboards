#!/usr/bin/env python

import os.path as op
import pyxnat
import logging as log
# import sys
# sys.path.insert(0, op.abspath('..'))


def create_args():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", type=argparse.FileType('r'),
                    help="Path to pyxnat configuration file",
                    required=True)
    ap.add_argument("-p", "--pickle", type=str,
                    help="Path where the pickle file will be created",
                    required=True)
    return ap


if __name__ == "__main__":
    parser = create_args()
    args = parser.parse_args()

    log.basicConfig(level=log.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s:%(module)s:%(levelname)s:%(message)s')

    config = args.config.name
    fp = op.abspath(args.pickle)

    from dashboards import pickle
    x = pyxnat.Interface(config=config)
    pickle.save(x, fp)
    x.close_jsession()
