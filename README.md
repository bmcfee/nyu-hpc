nyu-hpc
=======

Helper utilities for interacting with hpc.nyu.edu.  This includes things like:

* SSH tunneling
* Job deployment
* Fabulous prizes

Tunneling
=========
Probably, you'll want to fork this project and modify the scripts and configs for your exact setup.


IPython.Parallel
================

I'll assume that all parallel code will be written using IPython.

To make this work, you'll first need to generate a profile by saying

    ipython profile create --parallel --profile=mpi

and then modify `~/.ipython/profile_mpi/ipcluster_config.py` to include the line

    c.IPClusterEngines.engine_launcher_class = 'MPIEngineSetLauncher' 

