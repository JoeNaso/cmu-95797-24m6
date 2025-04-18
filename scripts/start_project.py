"""
Set up the project dependencies so the warehouse codebase runs on your local machine without issue
"""

import os
from pathlib import Path
import time
import subprocess


ENV = ".env"
VENV = ".venv"
THIS_PROJECT = Path(__file__).resolve().parent.parent


def _env():
    """
    Write a .env file
    """    
    if not os.path.exists(os.path.join(os.sep, THIS_PROJECT, ".env")):
        with open(THIS_PROJECT / ".env", 'w') as f:
            f.write("# Caution: if you change this value, your warehouse project may not work as expected")
            f.write(f"CMU_WH_LOCAL_SOURCE_DATA={THIS_PROJECT}/source_data/")


def _setup_env():
    """
    create a virtual env for later usage
    since we cant really write the required env vars into the activate script cleanly, users must source the env manually
    """
    venv_dir = os.path.join(os.sep, THIS_PROJECT, VENV)
    if os.path.exists(venv_dir):
        os.removedirs(venv_dir)
    if not os.getcwd() == THIS_PROJECT:
        os.chdir(THIS_PROJECT)
    subprocess.run(["uv", "venv", str(VENV)], check=True)

    subprocess.run(["uv", "pip", "install", "-r", "pyproject.toml"], check=True)




def welcome_message():
    banner = "Beginning CMU-85797 Warehouse setup..."
    one = "Please make sure you have downloaded the source data ZIP file and placed in the `source_data` folder of this project"
    two = "This script will set up an environment on your computer so you can run the project"
    three = "Refer to the `README.md` after this process completes."
    directions = [one, two, three]
    max_len = max(len(line) for line in directions)
    border = "=" * (len(one) + 4)
    print("\n" + border)
    for step in [banner, "", *directions]:
        print(f"| {step.ljust(max_len)} |")
        time.sleep(1)
    print(border + "\n")    


def start():
    _env()
    _setup_env()

    # welcome_message()




if __name__ == "__main__":
    start()