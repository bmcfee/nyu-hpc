nyu-hpc
=======

Helper utilities for interacting with hpc.nyu.edu.  This includes things like:

* SSH tunneling
* Job deployment
* Fabulous prizes


Tunneling
=========
Probably, you'll want to fork this project and modify the scripts and configs for your exact setup.


Python environment
==================

Once you're into HPC, you'll need to set up a sane python environment.

* First, you'll need to load the python module:

      ```
      module purge
      module add python
      ```

* Next, to make any of the IPython parallelism work, you'll need to install ZMQ.

  This can be done by first installing `pip` by following 
  [these instructions](https://pip.pypa.io/en/latest/installing.html).

* You'll need to add `~/.local/bin` to your `$PATH` environment variable by 
  editing `~/.bash_profile`.

* Finally, install the `zmq` module by saying

      ```
      pip install --user pyzmq
      ```

* Then, add the `mpi4py` module

      ```
      module add mpi4py
      ```

  and create an IPython cluster profile:

      ```
      ipython profile create --parallel --profile=mpi
      ```

  and then modify `~/.ipython/profile_mpi/ipcluster_config.py` to include the line

      ```
      c.IPClusterEngines.engine_launcher_class = 'MPIEngineSetLauncher' 
      ```


