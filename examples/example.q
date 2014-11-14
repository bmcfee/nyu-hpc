#!/bin/bash
#PBS -l nodes=3:ppn=4
#PBS -l walltime=1:00:00
#PBS -l mem=1GB
#PBS -N demo_script
#PBS -m ae
#PBS -M brian.mcfee@nyu.edu
#PBS -j oe

module purge
module add mpi4py scikit-learn theano pytables

# Needed environment variables.
# Locations.
export SRCDIR=$HOME/git/nyu-hpc/examples
export RUNDIR={results_root}
export PROFILEDIR=$RUNDIR/profile
mkdir -p $RUNDIR
cd $RUNDIR

# Set up and start the IPython cluster.
cp -r $HOME/.config/ipython/profile_mpi $PROFILEDIR
ipcluster start -n $PBS_NP --profile-dir=$PROFILEDIR &> ipcluster.log &

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
    python $SRCDIR/example_script.py --profile-dir $PROFILEDIR &> output.log
else
    echo "Server never started" &> output.log
fi

# Shut the cluster down.
ipcluster stop --profile-dir=$PROFILEDIR

exit $(( 1-success ));
