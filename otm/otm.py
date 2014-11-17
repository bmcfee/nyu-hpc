#!/usr/bin/env python

from __future__ import print_function
from argparse import ArgumentParser
import sys

import os
import jinja2


def process_arguments(args):

    parser = ArgumentParser(description='One, Two, Many. Deploy jobs on HPC.')

    parser.add_argument('-n', '--num_nodes',
                        dest='num_nodes',
                        type=int,
                        default=1,
                        help='Number of nodes to request')

    parser.add_argument('-c', '--num_cores',
                        dest='num_cores',
                        type=int,
                        default=4,
                        help='Number of cores per node to request')

    parser.add_argument('-t', '--run_time',
                        dest='run_time',
                        type=str,
                        default='4:00:00',
                        help='Maximum amount of time to let this job run')

    parser.add_argument('-m', '--memory',
                        dest='memory',
                        type=str,
                        default='2GB',
                        help='Amount of memory to request')

    parser.add_argument('--name',
                        dest='name',
                        type=str,
                        default=None,
                        help='Name for this job. Defaults to cmd[0]')

    parser.add_argument('-d', '--destination',
                        type=str,
                        required=True,
                        help='Directory to execute this job in')

    parser.add_argument('--modules',
                        dest='modules',
                        type=str,
                        default=None,
                        help='Path to a file listing modules to be included')

    parser.add_argument('-s', '--submit',
                        dest='submit',
                        default=False,
                        action='store_true',
                        help='Submit this job immediately')

    parser.add_argument('cmd',
                        nargs='+',
                        type=str,
                        help='Command line to execute')

    return vars(parser.parse_args(args))

if __name__ == '__main__':

    parameters = process_arguments(sys.argv[1:])

    print(parameters)
