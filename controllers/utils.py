import subprocess


def get_version():

    version = subprocess.check_output(["git", "describe", "--tags", "--long", "--always"]).strip()
    label = subprocess.check_output(["git", "show", "-s",  "--format=format:Author: %an%nDate: %cd"]).strip()

    return version.decode('utf-8') + "\n" + label.decode('utf-8')