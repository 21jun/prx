import subprocess
import argparse
import os
from pathlib import Path

from datetime import datetime
from utils.color import bcolors, print_color
from utils.db import save_job_log
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
        print_color(bcolors.HEADER, "[config]")
        print_color(
            bcolors.BOLD, "Found multiple .ini files in .prx directory.", end="\n"
        )
        print_color(bcolors.HEADER, "[config]")
        print_color(bcolors.BOLD, f"load the first one. {config_file[0]}", end="\n")

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


def exec_sbatch(config, args):
    # first, sync the files
    rsync.rsync_box(config=config, dry_run=args.dry, reverse_sync=args.reverse)
    # then, submit the job
    slurm.run_sbatch(config=config, sbatch_file_path=args.sbatch_file_path)


def exec_sremain(config, args):
    # then, submit the job
    slurm.run_sremain(config=config)


def exec_scontrol(config, args):
    slurm.run_scontrol(config=config, job_id=args.job_id)


def exec_rsync(config, args):
    rsync.rsync_box(config=config, dry_run=args.dry, reverse_sync=args.reverse)


def exec_sh(config, args):
    slurm.run_sh(config=config, command=args.command)


def exec_run(config, args):
    # First create run dir in local
    sbatch_file_path = run.create_run(config, args)
    # Then sync the files
    rsync.rsync_box(config=config, dry_run=args.dry)

    # Then submit the job
    jobid = slurm.run_sbatch(config=config, sbatch_file_path=sbatch_file_path)

    # save jobid

    logs = (
        str(Path(sbatch_file_path).absolute())
        + "\t"
        + args.gpu_type
        + " x "
        + args.gpu_num
        + "\t"
    )
    save_job_log(jobid, logs)


def main():
    # parse config at .prx directory (.ini)
    config = parse_config()

    # args for runtime
    main_parser = argparse.ArgumentParser(description="Main parser")
    subparsers = main_parser.add_subparsers(help="sub-command help", dest="command")

    init_parser = subparsers.add_parser("init", help="init help")
    init_parser.add_argument("--python_env", "-p", type=str, help="")

    sbatch_parser = subparsers.add_parser("sbatch", help="sbatch help")
    sbatch_parser.add_argument("--file", "-f", type=str, help="sbatch file")
    sbatch_parser.add_argument("--dry", action="store_true")

    sremain_parser = subparsers.add_parser("sremain", help="sremain help")
    sremain_parser.add_argument("--dry", action="store_true")

    sync_parser = subparsers.add_parser("sync", help="sync help")
    sync_parser.add_argument("--dry", action="store_true", default=False)
    sync_parser.add_argument(
        "--reverse",
        "-r",
        action="store_true",
        default=False,
        help="reverse sync from remote to local.)",
    )

    log_parser = subparsers.add_parser("log", help="log help")
    log_parser.add_argument("--job_id", "-j", type=str, default=None)

    sh_parser = subparsers.add_parser("sh", help="sh help")
    sh_parser.add_argument(
        "--sh", "-s", type=str, help="command to run, should be quoted('' or \"\")"
    )

    run_parser = subparsers.add_parser("run", help="run help")
    run_parser.add_argument("--file", "-f", type=str, help="sbatch file")
    run_parser.add_argument("--gpu_num", "-n", default="1")
    run_parser.add_argument("--gpu_type", "-t", default="A6000")
    run_parser.add_argument("--dry", action="store_true")

    test_parser = subparsers.add_parser("test", help="test help")
    test_parser.add_argument("--gpu_num", "-n", default="1")
    test_parser.add_argument("--gpu_type", "-t", default="A6000")

    args = main_parser.parse_args()

    print_color(bcolors.HEADER, "[main]")
    print_color(bcolors.HEADER, f"command: {args.command}", end="\n")
    # print what subcommand is called

    def switch_command(command, config, args):
        commands = {
            "init": init,
            "sbatch": exec_sbatch,
            "sremain": exec_sremain,
            "sync": exec_rsync,
            "log": exec_scontrol,
            "sh": exec_sh,
            "run": exec_run,
            "test": print,
        }
        return commands.get(command, lambda: print("Invalid command"))(config, args)

    switch_command(args.command, config=config, args=args)


if __name__ == "__main__":
    main()
