#!/bin/bash

# declare a name for this job to be sample_job
#PBS -N StructOptTest
#PBS -q morganshort
# request 1 processes
#PBS -l nodes=1:ppn=8,pvmem=2000mb
# request 48 hours of wall time
#PBS -l walltime=4:00:00
# combine PBS standard output and error files
##PBS -j oe
##PBS -k eo

#How many procs do I have?
NN=`cat $PBS_NODEFILE | wc -l`
echo "Processors received = "$NN
echo "script running on host `hostname`"

#cd into the directory where I typed qsub
cd $PBS_O_WORKDIR
echo "PBS_NODEFILE"
cat $PBS_NODEFILE

#Type in commands to run. Replace a.out with the program name
#to run.
LD_LIBRARY_PATH=//share/apps/mvapich2/tam_mvapich2-1.9a2/usr/local/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH
LAMMPS_COMMAND="//share/apps/mvapich2/tam_mvapich2-1.9a2/usr/local/bin/mpirun -n 1 /home/amyk/bin/lmp_linux"
export LAMMPS_COMMAND
//share/apps/mvapich2/tam_mvapich2-1.9a2/usr/local/bin/mpirun -n 8 //share/apps/EPD_64bit/epd_free-7.3-2-rh5-x86_64/bin/python run.py > output.txt



