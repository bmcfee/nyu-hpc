#!/bin/bash
#PBS -m ae
#PBS -j oe
#PBS -l nodes=1:ppn=4
#PBS -l walltime=1:00:00
#PBS -l mem=1GB
#PBS -N singlenode_multicore
#PBS -M brian.mcfee@nyu.edu

module purge
module add scikit-learn

# Needed environment variables.
# Locations.
export SRCDIR=$HOME/git/nyu-hpc/examples
export RUNDIR=$HOME/results_ex
mkdir -p $RUNDIR
cd $RUNDIR

# Set up and start the IPython cluster.
env |sort &> env.log

python $SRCDIR/singlenode_multicore.py \
                        --num_jobs $PBS_NP \
                        -v 3 \
    &> output.log

