import subprocess
import os

package_dir = os.path.dirname(os.path.abspath(__file__))


def rsync_box(config, dry_run=False, reverse_sync=False):

    SERVER = config["REMOTE"]["SERVER"]
    WORKDIR = config["REMOTE"]["WORKDIR"]
    HOME = config["REMOTE"]["HOME"]
    SOURCE = config["LOCAL"]["SOURCE"]
    DEST = config["REMOTE"]["DEST"]

    script_path = os.path.join(package_dir, "rsync_box.sh")

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
            "--reverse" if reverse_sync else "",
        ]
    ).communicate()
    # sub_proc.wait()
