import subprocess
import os
from utils.color import print_color, bcolors
import shutil
from pathlib import Path
from datetime import datetime
import re


def _extract_format_variables(template):
    pattern = r"\{(\w+)\}"
    matches = re.findall(pattern, template)
    return set(matches)

def fetch_run(config, args):
    
    SERVER = config["REMOTE"]["SERVER"]
    HOME = config["REMOTE"]["HOME"]
    CONDA_ENV = config["REMOTE"]["CONDA_ENV"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    # DEST = config["REMOTE"]["DEST"]
    print_color(bcolors.OKGREEN, "[fetch]")
    print(f"Fetching {args.run} from {SERVER}...")
    command = f"scp -r {SERVER}:{HOME}/{WORKDIR}/runs/{args.run} runs/"
    print(command)
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    print(result[0].decode())
    print_color(bcolors.OKGREEN, "\n[fetch]")
    print("Done.")

def create_run(config, args):
    DATETIME = datetime.now().strftime("%Y%m%d-%H%M%S")

    SCRIPT_PATH = args.file
    EXP_ROOT = Path(SCRIPT_PATH).parent

    RUN_PATH = EXP_ROOT / "runs" / f"run_{DATETIME}"
    # create run directory
    Path(RUN_PATH).mkdir(parents=True, exist_ok=True)

    # copy all files in the directory except the runs directory
    for file in os.listdir(EXP_ROOT):
        if file != "runs":
            shutil.copy2(EXP_ROOT / file, RUN_PATH)

    print_color(bcolors.OKCYAN, "[run]")
    print_color(bcolors.UNDERLINE, "[local]")
    print_color(bcolors.OKGREEN, f"Created run: {EXP_ROOT}/runs/", end="")
    print_color(bcolors.OKCYAN, f"{RUN_PATH.name}", end="\n")

    with open(".prx/template.sbatch", "r") as f:
        script_template = f.read()

    # replace the template with the config
    # for key in config["SLURM"]:
    #     print(key.upper(), config["SLURM"][key])
    #     script_template = script_template.format(JOB_NAME=config["SLURM"][key])
    variables = _extract_format_variables(script_template)
    # print(variables)

    # for key, val in config["SLURM"].items():
    #     print(key, val)

    mapping = {}
    # Magic keys
    mapping["RUN_SCRIPT_PATH"] = RUN_PATH / Path(SCRIPT_PATH).name
    mapping["RUN_PATH"] = RUN_PATH
    mapping["DATETIME"] = DATETIME
    mapping["EXP_NAME"] = EXP_ROOT.name
    mapping["OUTPUT_PATH"] = RUN_PATH
    mapping["JOB_NAME"] = f"{EXP_ROOT.name}_{DATETIME}"

    # overwrite the config if the key is defined in the config
    for key, val in config["SLURM"].items():
        mapping[key.upper()] = val

    mapping["GPU_TYPE"] = (
        args.gpu_type if args.gpu_type else config["SLURM"]["GPU_TYPE"]
    )
    mapping["GPU_NUM"] = args.gpu_num if args.gpu_num else config["SLURM"]["GPU_NUM"]

    for key, val in mapping.items():
        if val is None:
            print_color(
                bcolors.WARNING, f"Warning: {key} is not defined in the config file."
            )
            mapping[key] = input(f"{key} = ")

    # print(mapping)

    script_template = script_template.format(**mapping)


    sbatch_file_path = None

    with open(RUN_PATH / "run.sbatch", "w") as f:
        f.write(script_template)
        sbatch_file_path = f.name

    print_color(bcolors.OKCYAN, "[run]")
    print("complete.")
    return sbatch_file_path


def remove_run(config, args):
    pass


