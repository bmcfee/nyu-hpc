#!/usr/bin/env python
'''One, two, many.  Deploy jobs on HPC.'''

from __future__ import print_function
from argparse import ArgumentParser
import sys

import os
import subprocess
import datetime
import tempfile
import jinja2
import pkg_resources


def load_template(template=None, num_nodes=1):
    '''Load the template, either fixed or determined from # nodes'''

    if template is None:
        if num_nodes == 1:
            # Single-node
            template = pkg_resources.resource_filename(__name__,
                                                       'node_single.q.tpl')
        else:
            # Multi-node
            template = pkg_resources.resource_filename(__name__,
                                                       'node_multi.q.tpl')

    template = os.path.abspath(template)

    loader = jinja2.FileSystemLoader(os.path.dirname(template))
    env = jinja2.environment.Environment(loader=loader)

    return env.get_template(os.path.basename(template))


def load_modules(modfile):
    '''Load a list of module names'''

    modules = []

    if modfile is None:
        return modules

    try:
        with open(modfile, 'r') as file_desc:
            modules.extend([line.strip() for line in file_desc])
    except IOError:
        pass

    return modules


def mktmp(**kwargs):
    '''Wrapper for tempfile.mkstep'''

    fd, filename = tempfile.mkstemp(**kwargs)

    handle = os.fdopen(fd, 'w+b')

    return handle, filename


def create_qfile(tstr):
    '''Save the template file'''

    # First, check to see that we have an otm directory
    otmdir = os.sep.join([os.environ['HOME'], '.otm'])
    try:
        os.makedirs(otmdir)
    except OSError:
        pass

    timestamp = datetime.datetime.now()

    prefix = '{:04d}{:02d}{:02d}T{:02d}{:02d}{:02d}_'.format(timestamp.year,
                                                             timestamp.month,
                                                             timestamp.day,
                                                             timestamp.hour,
                                                             timestamp.minute,
                                                             timestamp.second)
    # Create a temporary file
    handle, qname = mktmp(dir=otmdir,
                          prefix=prefix,
                          suffix='{}q'.format(os.extsep))

    # Dump the rendered template
    handle.write(tstr)
    handle.close()

    # Return the filename
    return qname


def submit_job(qfile):
    '''Submit a job to the queuing engine'''

    print('Submitting job for queuing')
    subprocess.call(['qsub', qfile])


def main(**params):
    '''The main program'''

    # First, load the template

    template = load_template(num_nodes=params['num_nodes'],
                             template=params['template'])

    params['modules'] = load_modules(params['module_file'])

    tstr = template.render(**params)

    qfile = create_qfile(tstr)

    print('Rendered PBS script to {:s}'.format(qfile))

    if params['submit']:
        # Submit the job
        submit_job(qfile)


def process_arguments(args):
    '''Process command-line arguments'''

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
                        type=unicode,
                        default='4:00:00',
                        help='Maximum amount of time to let this job run')

    parser.add_argument('-m', '--memory',
                        dest='memory',
                        type=unicode,
                        default='4GB',
                        help='Amount of memory to request')

    parser.add_argument('--name',
                        dest='name',
                        type=unicode,
                        default=None,
                        help='Name for this job. Defaults to cmd[0]')

    parser.add_argument('-d', '--destination',
                        type=unicode,
                        required=True,
                        help='Directory to execute this job in')

    parser.add_argument('--modules',
                        dest='module_file',
                        type=unicode,
                        default=None,
                        help='Path to a file listing modules to be included')

    parser.add_argument('-s', '--submit',
                        dest='submit',
                        default=False,
                        action='store_true',
                        help='Submit this job immediately')

    parser.add_argument('--template',
                        dest='template',
                        type=unicode,
                        default=None,
                        help='Path to the PBS script template')

    parser.add_agrument('--gpu',
                        dest='gpu',
                        default=False,
                        action='store_true',
                        help='Require a GPU on the node')

    parser.add_argument('cmd',
                        nargs='+',
                        type=str,
                        help='Command line to execute')

    params = vars(parser.parse_args(args))

    if params['name'] is None:
        params['name'] = os.path.basename(params['cmd'][0])

    params['cmds'] = u' '.join(params['cmd'])
    del params['cmd']

    return params


if __name__ == '__main__':

    parameters = process_arguments(sys.argv[1:])

    main(**parameters)
