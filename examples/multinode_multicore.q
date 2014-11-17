#!/bin/bash
#PBS -l nodes=1:ppn=4
##PBS -l nodes=2:ppn=2 -W x=nmatchpolicy:exactnode
#PBS -l walltime=1:00:00
#PBS -l mem=1GB
#PBS -N demo_script
#PBS -m ae
#PBS -M brian.mcfee@nyu.edu
#PBS -j oe

module purge
module add mpi4py

# Needed environment variables.
# Locations.
export SRCDIR=$HOME/git/nyu-hpc/examples
export RUNDIR=$HOME/results_ex
export PROFILEDIR=$RUNDIR/profile
# export PROFILEDIR=$HOME/.config/ipython/profile_mpi
mkdir -p $RUNDIR
cd $RUNDIR

# Set up and start the IPython cluster.
env |sort &> env.log
cp -r $HOME/.config/ipython/profile_mpi $PROFILEDIR
ipcluster start -n $PBS_NP \
                --profile-dir=$PROFILEDIR \
                --controller=MPI \
                --engines=MPI \
    &> ipcluster.log &

sleep 5
for (( try=0; try < 100; ++try )); do
    if cat ipcluster.log | grep -q "Engines appear to have started successfully"; then
        success=1
        break
    fi
    sleep 5
done

if (( success )); then
    # Run the analysis.
    python $SRCDIR/multinode_multicore.py --profile-dir $PROFILEDIR &> output.log
else
    echo "Server never started" &> output.log
fi

# Shut the cluster down.
ipcluster stop --profile-dir=$PROFILEDIR

exit $(( 1-success ));
