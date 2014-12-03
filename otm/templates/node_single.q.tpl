#!/bin/bash
#PBS -m ae
#PBS -j oe
{% if gpu %}
#PBS -l nodes={{ num_nodes }}:ppn={{ num_cores }}:gpus={{ num_gpu_cores }}
{% else %}
#PBS -l nodes={{ num_nodes }}:ppn={{ num_cores }}
{% endif %}
#PBS -l walltime={{ run_time }}
#PBS -l mem={{ memory }}
#PBS -N {{ name }}
{% if email %}
#PBS -M {{ email }}
{% endif %}

# Built by otm.py with the following command line:
# {{ CMDLINE|wordwrap(width=60, break_long_words=False, wrapstring=' \\\n# \t')}}

# Clear the modules
module purge

{% for mod in modules %}
module add {{ mod }}
{% endfor %}

# Move into the running path
export RUNDIR={{ destination }}
mkdir -p $RUNDIR

cd $RUNDIR

# Dump the environment variables
env |sort &> env.log

# Execute the command
{{ cmds }}

