# -*- coding: utf-8 -*-
import logging as l
import argparse
import os
import sys
import json

import numpy as np
import scipy.sparse as ss
import scipy.io as sio
import pandas as pd
import jsonnet

from ume.utils import feature_functions, save_mat, dynamic_load, load_settings
from ume.visualize import Plot


def parse_args():
    p = argparse.ArgumentParser(
        description='CLI interface UME')
    p.add_argument('--config', dest='inifile', default='config.ini')

    subparsers = p.add_subparsers(
        dest='subparser_name',
        help='sub-commands for instant action')

    f_parser = subparsers.add_parser('feature')
    f_parser.add_argument('-a', '--all', action='store_true', default=False)
    f_parser.add_argument('-n', '--name', type=str, required=True)

    subparsers.add_parser('init')

    v_parser = subparsers.add_parser('validate')
    v_parser.add_argument(
        '-m', '--model',
        required=True,
        type=str,
        help='model description file described by json format')

    z_parser = subparsers.add_parser('visualize')
    z_parser.add_argument('-j', '--json', type=str, required=True)
    z_parser.add_argument('-o', '--output', type=str, required=True)

    p_parser = subparsers.add_parser('predict')
    p_parser.add_argument(
        '-m', '--model',
        required=True,
        type=str,
        help='model description file described by json format')
    p_parser.add_argument(
        '-o', '--output',
        required=True,
        type=str,
        help='output file')

    return p.parse_args()


def run_visualization(args):
    if args.json.endswith(".jsonnet"):
        config = json.loads(jsonnet.load(args.json).decode())
    else:
        with open(args.json, 'r') as f:
            config = json.load(f)

    title_name = config['title'] if 'title' in config else ""
    p = Plot(title=title_name)
    data_dict = {}
    for source_name in config['datasource'].keys():
        data_dict[source_name] = pd.read_csv(config['datasource'][source_name])

    for i, plotdata in enumerate(config['plotdata']):
        if 'plot' not in plotdata:
            continue  # empty space

        for j, plate in enumerate(plotdata['plot']):
            plate_source = data_dict[plate['source']]
            for ax_name in ['X', 'y']:
                if ax_name == 'y' and ax_name not in plate:
                    # plate_hist doesn't require y-axis.
                    config['plotdata'][i]['plot'][j][ax_name] = None
                else:
                    col = plate[ax_name]
                    config['plotdata'][i]['plot'][j][ax_name] = plate_source[col]

    layout_param = {} if 'layout' not in config else config['layout']

    for c in config['plotdata']:
        p.add(c)
    p.save(args.output, **layout_param)


def run_feature(args):
    if args.all is True:
        print(args.name)
        mod, names = feature_functions(args.name)
        for name in names:
            target = "{0}.{1}".format(args.name, name)
            l.info("Feature generation: {0}".format(target))
            func = getattr(mod, name)
            result = func()
            save_mat(target, result)
    else:
        l.info("Feature generation: {0}".format(args.name))
        klass = dynamic_load(args.name)
        result = klass()
        save_mat(args.name, result)


def run_initialize(args):
    pwd = os.getcwd()
    os.makedirs(os.path.join(pwd, "data/input/model"))
    os.makedirs(os.path.join(pwd, "data/input/visualize"))
    os.makedirs(os.path.join(pwd, "data/output"))
    os.makedirs(os.path.join(pwd, "data/output/visualize"))
    os.makedirs(os.path.join(pwd, "data/working"))
    os.makedirs(os.path.join(pwd, "note"))
    os.makedirs(os.path.join(pwd, "trunk"))


def _load_features(f_names):
    X = None
    for f_name in f_names:
        l.info(f_name)
        var_name = 'X'
        if type(f_name) is dict:
            var_name = f_name['name']
            f_name = f_name['file']

        X_add = sio.loadmat(f_name)[var_name]
        if X is None:
            X = X_add
        elif type(X) is np.ndarray and type(X_add) is np.ndarray:
            X = np.hstack((X, X_add))
        else:
            X = X_add if X is None else ss.hstack((X, X_add))
    return X


def _load_train_test(settings):
    X = _load_features(settings['features'])
    idx_train = sio.loadmat(settings['idx']['train']['file'])[
        settings['idx']['train']['name']
    ]
    idx_test = sio.loadmat(settings['idx']['test']['file'])[
        settings['idx']['test']['name']
    ]
    idx_train = idx_train[:, 0]
    idx_test = idx_test[:, 0]
    X_train = X[idx_train]
    X_test = X[idx_test]
    y_train = sio.loadmat(settings['target']['file'])[
        settings['target']['name']
    ]
    #y_train = y_train[:, 0, 0]
    y_train = y_train[:, 0]
    return X_train, X_test, y_train


def run_validation(args):
    settings = load_settings(args.model)
    l.info("Loading dataset")
    X, _, y = _load_train_test(settings)
    kfoldcv = dynamic_load(settings['cross_validation']['method'])
    score, variance = kfoldcv(X, y, settings)
    l.info("CV score: {0:.4f} (var: {1:.6f})".format(score, variance))


def run_prediction(args):
    settings = load_settings(args.model)
    prediction = settings['prediction']
    l.info("Loading dataset")
    X_train, X_test, y_train = _load_train_test(settings)

    predict_klass = dynamic_load(prediction['method'])
    p = predict_klass(settings)
    y_pred = p.solve(X_train, X_test, y_train)

    pd.DataFrame({'y_pred': y_pred}).to_csv(args.output, index=False)


def run_version_checker(args):
    pass


def main():
    l.basicConfig(format='%(asctime)s %(message)s', level=l.INFO)
    sys.path.append(os.getcwd())
    args = parse_args()
    if args.subparser_name == 'validate':
        run_validation(args)
    elif args.subparser_name == 'visualize':
        run_visualization(args)
    elif args.subparser_name == 'predict':
        run_prediction(args)
    elif args.subparser_name == 'feature':
        run_feature(args)
    elif args.subparser_name == 'init':
        run_initialize(args)
    elif args.subparser_name == 'version':
        run_version_checker(args)
    else:
        raise RuntimeError("No such sub-command.")
