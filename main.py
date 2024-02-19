import subprocess
import argparse
import os

from datetime import datetime
from utils.color import bcolors, print_color
import glob
import sys
from src import rsync
from src import slurm
from src import run
import configparser

package_dir = os.path.dirname(os.path.abspath(__file__))


def parse_config():
    # find .ini file in .prx directory
    config_file = sorted(list(glob.glob(".prx/*.ini")))
    
    if len(config_file) > 1:
        print_color(bcolors.WARNING, "Found multiple .ini files in .prx directory.", end="\n")
        print_color(bcolors.HEADER, "[config]")
        print_color(bcolors.WARNING, f"load the first one. {config_file[0]}", end="\n")
        

    print_color(bcolors.HEADER, "[config]")
    config_file = config_file[0]
    print(f"config file: {config_file}")
    config = configparser.ConfigParser()
    config.read(config_file)
    # print(config["REMOTE"]["SERVER"])

    # iter over sections
    for section in config.sections():
        # print(bcolors.HEADER + f"[{section}]" + bcolors.ENDC)
        for key in config[section]:
            ...
            # print(f"{key.upper()} = {config[section][key]}")

    return config


def init(config):

    def load_template():
        with open(f"{package_dir}/.prx/template.ini", "r") as f:
            template = f.read()


        # make directory in local
        if not os.path.exists(".prx"):
            os.mkdir(".prx")

        print_color(bcolors.HEADER, "[init]")
        input("Creating .prx/default.ini. Press Enter to continue...")
        python_env = input("Python environment (default: ~/anaconda3/base): ")
        python_env = python_env if python_env else "~/anaconda3/base"

        
        template = template.replace("{{python_env}}", python_env)

        
        

        with open(".prx/default.ini", "w") as f:
            f.write(template)

     
        print_color(bcolors.HEADER, "[init]")
        print_color(bcolors.HEADER, "Created .prx/default.ini", end="\n")
        

    # make directory in remote
    def check_dir(config):
        SERVER = config["REMOTE"]["SERVER"]
        HOME = config["REMOTE"]["HOME"]
        WORKDIR = config["REMOTE"]["WORKDIR"]

        command = f"ssh {SERVER} '. {HOME}/.bashrc; ls {HOME}/{WORKDIR}/;'"
        result = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()
        rp = result[0].decode()
        print(rp)

    def run_mkdir(config):
        SERVER = config["REMOTE"]["SERVER"]
        HOME = config["REMOTE"]["HOME"]
        WORKDIR = config["REMOTE"]["WORKDIR"]

        command = (
            f"ssh {SERVER} '. {HOME}/.bashrc; mkdir -p {HOME}/{WORKDIR}/; pwd;'"  # noqa
        )
        # command = f"ssh {SERVER} '. {HOME}/.bashrc; ls {HOME}/{WORKDIR}/;'"  # noqa
        result = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()
        rp = result[0].decode()
        print(rp)
        print("Done.")


    tamplate = load_template()
    print(tamplate)

    # check_dir(config)
    # run_mkdir(config)


# Recipes

def exec_sbatch(config, sbatch_file_path, dry_run=False, reverse_sync=False):
    # first, sync the files
    rsync.rsync_box(config=config, dry_run=dry_run, reverse_sync=reverse_sync)
    # then, submit the job
    slurm.run_sbatch(config=config, sbatch_file_path=sbatch_file_path)


def exec_sremain(config, debug=False):
    # then, submit the job
    slurm.run_sremain(config=config)

def exec_scontrol(config, job_id):
    slurm.run_scontrol(config=config, job_id=job_id)


def exec_rsync(config, dry_run=False, reverse_sync=False):
    rsync.rsync_box(config=config, dry_run=dry_run, reverse_sync=reverse_sync)

def exec_sh(config, command):
    slurm.run_sh(config=config, command=command)

def exec_run(config, args):
    
    # First create run dir in local
    run.create_run(config, args)
    # Then sync the files
    rsync.rsync_box(config=config, dry_run=args.dry)

    # Then submit the job


def main():
    # parse config at .prx directory (.ini)
    config = parse_config()

    # config for runtime
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["init", "sme", "sbatch", "sremain", "sync", "log", "sh", "run", "test"],
        help="Subcommand to execute",
    )
    
    # parser.add_argument('args', nargs=argparse.REMAINDER, help="Additional arguments")
    parser.add_argument("--dry", action="store_true")
    parser.add_argument("--reverse", "-r", action="store_true")
    parser.add_argument("--nosync", action="store_true")
    parser.add_argument("--file", "-f", type=str, help="sbatch file")
    parser.add_argument("--sh", "-s", type=str, help="command to run, should be quoted('' or \"\")")
    parser.add_argument("--job_id", "-j", type=str, default=None)
    parser.add_argument("--option", "-o", type=str, default=None)
    args = parser.parse_args()
    
    command = args.command
    if command == "init":
        init(config)
    elif command == "sme":
        slurm.run_sme(config, args.option)
    elif command == "sbatch":
        exec_sbatch(config, sbatch_file_path=args.file, dry_run=args.dry)
    elif command == "sremain":
        exec_sremain(config)
    elif command == "sync":
        exec_rsync(config, dry_run=args.dry, reverse_sync=args.reverse)
    elif command == "log":
        exec_scontrol(config, job_id=args.job_id)
    elif command == "sh":
        exec_sh(config, command=args.sh)
    elif command == "run":
        
        # parser.add_argument("--gpu_num", "-n", default=configurations["GPU_NUM"])
        # parser.add_argument("--gpu_type", "-t", default=configurations["GPU_TYPE"])
        args = parser.parse_args()

        exec_run(config, args)
    elif command == "test":
        parser.add_argument("--gpu_num", "-n", default="1")
        parser.add_argument("--gpu_type", "-t", default="A6000")
        args = parser.parse_args()
        print(args)
    else:
        print("Unknown command:", command)
        exit(1)

    # exec_sbatch(config, sbatch_file_path=args.file, dry_run=args.dry)
    # slurm.run_sme(config)
    # exec_sbatch(config, dry_run=args.dry)


if __name__ == "__main__":
    main()
