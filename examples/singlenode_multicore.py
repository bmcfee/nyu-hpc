#!/usr/bin/env python

from argparse import ArgumentParser
import sys
import os

from joblib import Parallel, delayed


def process_arguments(args):

    parser = ArgumentParser(description='Single-node, multi-core example')

    parser.add_argument('-n', '--num_cores',
                        dest='num_cores',
                        type=int,
                        default=2,
                        help='Number of cores to run in parallel')

    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        type=int,
                        default=0,
                        help='Verbosity level')

    parser.add_argument('-m', '--num_jobs',
                        dest='num_jobs',
                        type=int,
                        default=30,
                        help='Number of jobs to run total')

    return vars(parser.parse_args(args))


def myfunc(n):

    return "Job {:3d}: {:s}\t{:10d}\n".format(n,
                                              '-'.join(os.uname()),
                                              os.getpid())


def run_example(num_cores=2, num_jobs=30, verbose=0):

    for v in Parallel(n_jobs=num_cores,
                      verbose=verbose)(delayed(myfunc)(n)
                                       for n in range(num_jobs)):

        print v

if __name__ == '__main__':

    parameters = process_arguments(sys.argv[1:])

    run_example(**parameters)
