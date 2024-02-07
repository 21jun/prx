import subprocess
import argparse
import os

from datetime import datetime
from utils.color import bcolors, print_color
import glob
import sys
from src import rsync
from src import slurm
import configparser

package_dir = os.path.dirname(os.path.abspath(__file__))


def parse_config():
    print_color(bcolors.HEADER, "[config]")
    # find .ini file in .prx directory
    config_file = list(glob.glob(".prx/*.ini"))[0]

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

    print_color(bcolors.HEADER, "[config]")
    print("Done.")
    return config


def init(config):
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

    # check_dir(config)
    run_mkdir(config)


def exec_sbatch(config, sbatch_file_path, dry_run=False):
    # first, sync the files
    rsync.rsync_box(config=config, dry_run=dry_run)
    # then, submit the job
    slurm.run_sbatch(config=config, sbatch_file_path=sbatch_file_path)


def exec_sremain(config, debug=False):
    # then, submit the job
    slurm.run_sremain(config=config)


def exec_rsync(config, dry_run=False):
    rsync.rsync_box(config=config, dry_run=dry_run)


def main():
    # parse config at .prx directory (.ini)
    config = parse_config()

    # config for runtime
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["init", "sme", "run", "sremain", "sync"],
        help="Subcommand to execute",
    )
    # parser.add_argument('args', nargs=argparse.REMAINDER, help="Additional arguments")
    parser.add_argument("--dry", action="store_true")
    parser.add_argument("--nosync", action="store_true")
    parser.add_argument("--file", "-f", type=str, help="sbatch file")
    args = parser.parse_args()

    command = args.command
    if command == "init":
        init(config)
    elif command == "sme":
        slurm.run_sme(config)
    elif command == "run":
        exec_sbatch(config, sbatch_file_path=args.file, dry_run=args.dry)
    elif command == "sremain":
        exec_sremain(config)
    elif command == "sync":
        exec_rsync(config, dry_run=args.dry)
    else:
        print("Unknown command:", command)
        exit(1)

    # exec_sbatch(config, sbatch_file_path=args.file, dry_run=args.dry)
    # slurm.run_sme(config)
    # exec_sbatch(config, dry_run=args.dry)


if __name__ == "__main__":
    main()
