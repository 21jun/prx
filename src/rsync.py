import subprocess
import os
from utils.color import print_color, bcolors

package_dir = os.path.dirname(os.path.abspath(__file__))


def rsync_box(config, dry_run=False, reverse_sync=False):
    SERVER = config["REMOTE"]["SERVER"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    HOME = config["REMOTE"]["HOME"]
    SOURCE = config["LOCAL"]["SOURCE"]
    DEST = config["REMOTE"]["DEST"]

    script_path = os.path.join(package_dir, "rsync_box.sh")

    WORKDIR = HOME + "/" + WORKDIR
    prefix = '[rsync]'
    sub_proc = subprocess.Popen(
        [
            "sh",
            script_path,
            SERVER,
            WORKDIR,
            SOURCE,
            DEST,
            "--dry-run" if dry_run else "",
            "--reverse" if reverse_sync else "",
        ],
    ).communicate()
    # sub_proc.wait()

    # for line in sub_proc.stdout:
    #     print_color(bcolors.OKCYAN, prefix, end=' ')
    #     print(line, end='') 
    # sub_proc.wait()
    # .communicate()

def rsync_fetch(config, dry_run=False, path=None):
    SERVER = config["REMOTE"]["SERVER"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    HOME = config["REMOTE"]["HOME"]


    # SOURCE = config["LOCAL"]["SOURCE"]
    SOURCE = path
    DEST = path
    # DEST = config["REMOTE"]["DEST"]


    script_path = os.path.join(package_dir, "rsync_fetch.sh")

    print(script_path,
        SERVER,
        WORKDIR,
        SOURCE,
        DEST,)


    WORKDIR = HOME + "/" + WORKDIR
    sub_proc = subprocess.Popen(
        [
            "sh",
            script_path,
            SERVER,
            WORKDIR,
            SOURCE,
            DEST,
            "--dry-run" if dry_run else "",
        ],
      ).communicate()
    # sub_proc.wait()