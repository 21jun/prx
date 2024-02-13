import subprocess
import os
from utils.color import print_color, bcolors


def run_sremain(config, debug=False):
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]
    CONDA_ENV = config["REMOTE"]["CONDA_ENV"]
    command = f"ssh {SERVER} '. {HOME}/.bashrc; conda activate {HOME}/anaconda3/envs/{CONDA_ENV}; sremain;'"  # noqa

    print_color(bcolors.OKGREEN, "[sremain]")
    print(f"Connecting to {SERVER}...")

    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    rp = result[0].decode()
    print(rp)
    print_color(bcolors.OKGREEN, "[sremain]")
    print("Done.")

def run_sh(config, command):
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]
    CONDA_ENV = config["REMOTE"]["CONDA_ENV"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    # DEST = config["REMOTE"]["DEST"]
    print_color(bcolors.OKGREEN, "[sh]")
    print(f"Running [{command}] on {SERVER}...")
    command = f"ssh {SERVER} '. {HOME}/.bashrc; cd {HOME}/{WORKDIR}; conda activate {HOME}/anaconda3/envs/{CONDA_ENV}; {command};'"  # noqa
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    print(result[0].decode().strip())
    print_color(bcolors.OKGREEN, "[sh]")
    print("Done.")
    # print(rp)


def run_sbatch(config, sbatch_file_path):
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]
    CONDA_ENV = config["REMOTE"]["CONDA_ENV"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    # DEST = config["REMOTE"]["DEST"]
    print_color(bcolors.OKGREEN, "[sbatch]")
    # print(bcolors.OKGREEN + "[sbatch]" + bcolors.ENDC, end=" ")
    print(f"Submitting {sbatch_file_path} to {SERVER}...")
    command = f"ssh {SERVER} '. {HOME}/.bashrc; cd {HOME}/{WORKDIR}; conda activate {HOME}/anaconda3/envs/{CONDA_ENV}; sbatch {HOME}/{WORKDIR}/{sbatch_file_path};'"  # noqa
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    print(result[0].decode().strip())
    print_color(bcolors.OKGREEN, "[sbatch]")
    print("Done.")
    # print(rp)


def run_sme(config):
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]
    CONDA_ENV = config["REMOTE"]["CONDA_ENV"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    # DEST = config["REMOTE"]["DEST"]
    print_color(bcolors.OKGREEN, "[sme]")
    print(f"your current jobs are...")
    command = f"ssh {SERVER} '. {HOME}/.bashrc; sqeueu | grep $USER;'"  # noqa
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    print(result[0].decode().strip())
    print_color(bcolors.OKGREEN, "[sme]")
    print("Done.")
    # print(rp)


def run_scontrol(config, job_id):
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]

    print_color(bcolors.OKGREEN, "[scontrol]")
    print(f"Slurm logs... {job_id}")
    command = f"ssh {SERVER} '. {HOME}/.bashrc; scontrol show job {job_id} | grep StdOut | xargs | cut -d'=' -f2 | xargs cat;' "  # noqa
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    print(result[0].decode().strip())
    print_color(bcolors.OKGREEN, "[sme]")
    print("Done.")
    # print(rp)
    # scontrol show job 195992 | grep StdOut | xargs | cut -d'=' -f1


# It works.
# ssh cluster-ai ". ~/.bashrc; conda info --envs; conda activate /home1/lee1jun/anaconda3/envs/wav2ipa; sremain;"
