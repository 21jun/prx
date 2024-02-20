#!/bin/sh
#SBATCH -J {JOB_NAME} # job name
#SBATCH -o {OUTPUT_PATH}/%x.%j.out 
#SBATCH -p {GPU_TYPE} # queue name or partiton name
#SBATCH -t 72:00:00 # Run time (hh:mm:ss)
#SBATCH  --gres=gpu:{GPU_NUM}
#SBATCH  --nodes=1
#SBATCH  --ntasks=1
#SBATCH  --tasks-per-node=1
#SBATCH  --cpus-per-task={CPU_NUM}

date
module purge
echo $CONDA_DEFAULT_ENV
echo $CUDA_VISIBLE_DEVICES


cat {RUN_SCRIPT_PATH}
sh {RUN_SCRIPT_PATH} {GPU_NUM} {RUN_PATH}/checkpoints {LOG_PATH} {DATETIME} {EXP_NAME}



date