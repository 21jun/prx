import subprocess
import os
from utils.color import print_color, bcolors
import shutil
from pathlib import Path
from datetime import datetime


def build_sbatch_sciprt(config, args):
    with open(".prx/template.sbatch", "r") as f:
        script = f.read()

    # replace the template with the config
    for section in config.sections():
        for key in config[section]:
            script = script.replace(f"{{{{ {key.upper()} }}}}", config[section][key])


def create_run(config, args):
    DATETIME = datetime.now().strftime("%Y%m%d+%H:%M:%S")

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
