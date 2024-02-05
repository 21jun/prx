#!/bin/bash
#SBATCH -J es_20230530+15:06:07 # job name
#SBATCH -o /home1/lee1jun/develop/prx-test/out/output_%x.%j.out 
#SBATCH -p A5000 # queue name or partiton name
#SBATCH -t 72:00:00 # Run time (hh:mm:ss)
#SBATCH  --gres=gpu:1
#SBATCH  --nodes=1
#SBATCH  --ntasks=1
#SBATCH  --tasks-per-node=1
#SBATCH  --cpus-per-task=16

srun -l /bin/hostname
srun -l /bin/pwd
srun -l /bin/date

module purge
pip freeze

echo $CONDA_DEFAULT_ENV
echo $CONDA_PREFIX

date
echo $CUDA_VISIBLE_DEVICES
BASEDIR=$(dirname "$0")
echo $BASEDIR
