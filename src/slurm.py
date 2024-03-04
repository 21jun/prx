import subprocess
import os
from utils.color import print_color, bcolors


def run_sremain(config, debug=False):
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]
    CONDA_ENV = config["REMOTE"]["CONDA_ENV"]
    command = (
        f"ssh {SERVER} '. {HOME}/.bashrc; conda activate {CONDA_ENV}; sremain;'"  # noqa
    )
    print_color(bcolors.OKGREEN, "[sremain]")
    print(f"Connecting to {SERVER}...")

    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()

    print(f"\n{result[0].decode().strip()}\n")
    print_color(bcolors.OKGREEN, "[sremain]")
    print("Done.")


def run_sh(config, command):
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]
    CONDA_ENV = config["REMOTE"]["CONDA_ENV"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    # DEST = config["REMOTE"]["DEST"]
    print_color(bcolors.OKGREEN, "[sh]")
    print(f"Running [{command}] on {SERVER}...\n")
    command = f"ssh {SERVER} '. {HOME}/.bashrc; cd {HOME}/{WORKDIR}; conda activate {CONDA_ENV}; {command};'"  # noqa

    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    print(result[0].decode())
    print_color(bcolors.OKGREEN, "\n[sh]")
    print("Done.")


def run_sbatch(config, sbatch_file_path):
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]
    CONDA_ENV = config["REMOTE"]["CONDA_ENV"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    # DEST = config["REMOTE"]["DEST"]
    print_color(bcolors.OKGREEN, "[sbatch]")
    # print(bcolors.OKGREEN + "[sbatch]" + bcolors.ENDC, end=" ")
    print(f"Submitting {sbatch_file_path} to {SERVER}...")
    command = f"ssh {SERVER} '. {HOME}/.bashrc; cd {HOME}/{WORKDIR}; conda activate {CONDA_ENV}; sbatch {sbatch_file_path};'"  # noqa

    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    print_color(bcolors.OKGREEN, "[sbatch]")
    print(result[0].decode().strip())
    # Submitted batch job 202090
    # parse only the job id
    jobid = result[0].decode().strip().split()[-1]

    # check the jobid is number
    if not jobid.isdigit():
        print_color(bcolors.FAIL, "[sbatch]")
        print_color(bcolors.FAIL, "Failed to submit the job.", end="\n")
        return None

    print_color(bcolors.OKGREEN, "[sbatch]")

    return jobid


def run_squeue(config, option):
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]
    CONDA_ENV = config["REMOTE"]["CONDA_ENV"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    # DEST = config["REMOTE"]["DEST"]
    print_color(bcolors.OKGREEN, "[sme]")
    print(f"your current jobs are...")

    format = '"%6i  %30j  %9T %12u %8g %12P %4D %15R %4C %13b %8m %11l %11L %20p"'
    if option is not None:
        command = f"ssh {SERVER} '. {HOME}/.bashrc; squeue --format {format} | grep {option};'"
    else:
        command = f"ssh {SERVER} '. {HOME}/.bashrc; squeue --format {format};'"  # noqa

    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    print(f"\n{result[0].decode().strip()}\n")
    print_color(bcolors.OKGREEN, "[sme]")
    print("Done.")


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
    print(f"\n{result[0].decode().strip()}\n")
    print_color(bcolors.OKGREEN, "[sme]")
    print("Done.")
    # scontrol show job 195992 | grep StdOut | xargs | cut -d'=' -f1


# It works.
# ssh cluster-ai ". ~/.bashrc; conda info --envs; conda activate /home1/lee1jun/.conda/envs/wav2ipa; sremain;"
