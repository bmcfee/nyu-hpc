#!/bin/bash
#PBS -m ae
#PBS -j oe
#PBS -l nodes={{ num_nodes }}:ppn={{ num_cores }}
#PBS -l walltime={{ run_time }}
#PBS -l mem={{ memory }}
#PBS -N {{ name }}
{% if email %}
#PBS -M {{ email }}
{% endif %}

# Built by otm.py with the following command line:
# {{ CMDLINE }}

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
