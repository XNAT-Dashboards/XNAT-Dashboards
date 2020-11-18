#!/usr/bin/env python
import os.path as op
import pyxnat


def create_args():

    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--config", type=argparse.FileType('r'),
                    help="Path to pyxnat configuration file",
                    required=True)
    ap.add_argument("-o", "--pickle", type=argparse.FileType('w'),
                    help="Path where the pickle file will be created",
                    required=True)
    return ap


if __name__ == "__main__":
    parser = create_args()
    args = parser.parse_args()

    config = args.config.name
    fp = op.abspath(args.pickle.name)

    from xnat_dashboards import pickle
    x = pyxnat.Interface(config=config)
    pickle.save(x, fp)
