"""
Set up the project dependencies so the warehouse codebase runs on your local machine without issue
"""

import os
import json
from pathlib import Path
import time
import subprocess
import shutil
import platform


ENV = ".env"
VENV = ".venv"
PY_VERSION = "python3.11"
THIS_PROJECT = Path(__file__).resolve().parent.parent


def _msg(steps: list[str], max_len: int) -> None:
    for step in steps:
        print(f"| {step.ljust(max_len)} |")
        time.sleep(1)


def _env():
    """
    Write a .env file
    """
    if not os.path.exists(os.path.join(os.sep, THIS_PROJECT, ".env")):
        with open(THIS_PROJECT / ".env", "w") as f:
            f.write(
                "# Caution: if you change this value, your warehouse project may not work as expected"
            )
            f.write(f"CMU_WH_LOCAL_SOURCE_DATA={THIS_PROJECT}/source_data/")


def _setup_env():
    """
    create a virtual env for later usage
    since we cant really write the required env vars into the activate script cleanly, users must source the env manually
    """
    local_uv = subprocess.run(
        ["which", "uv"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if local_uv.stderr != "":
        raise ValueError(
            "Please make sure you install `uv` ony our computer before running this setup command\n",
            "Install instructions: \n\t[Windows] https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2",
            "\n\t[Mac] https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1",
        )
    uv_path = local_uv.stdout.strip()

    venv_dir = os.path.join(os.sep, THIS_PROJECT, VENV)
    if os.path.exists(venv_dir):
        shutil.rmtree(venv_dir)
    if not os.getcwd() == THIS_PROJECT:
        os.chdir(THIS_PROJECT)
    subprocess.run(
        [f"{uv_path}", "venv", VENV, f"--python={PY_VERSION}"],
        check=True,
        stdout=subprocess.PIPE,
    )
    installs = [
        f"{uv_path}",
        "pip",
        "install",
        "-r",
        "pyproject.toml",
    ]

    subprocess.run(
        installs,
        env={"VIRTUAL_ENV": venv_dir},
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _settings_json():
    machine = platform.system()
    # mac
    if machine.lower() == "darwin" or machine.lower() != "windows":
        paths = {
            "INTERPRETER_PATH": ".venv/bin/python",
            "DBT_EXECUTABLE": "${workspaceFolder}/.venv/bin/dbt",
        }
    else:
        paths = {
            "INTERPRETER_PATH": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
            "DBT_EXECUTABLE": "${workspaceFolder}\\.venv\\Scripts\\dbt.bat",
        }

    template = {
        "python.defaultInterpreterPath": paths.get("INTERPRETER_PATH"),
        "editor.formatOnSave": True,
        "[jinja]": {"editor.defaultFormatter": "ms-python.black-formatter"},
        "[sql]": {"editor.defaultFormatter": "sqlfluff.sqlfluff"},
        "dbtPowerUser.projectRoot": "${workspaceFolder}",
        "dbtPowerUser.dbtExecutablePath": paths.get("DBT_EXECUTABLE"),
        "dbtPowerUser.enableHoverDocumentation": True,
        "dbtPowerUser.enableModelGraph": True,
        "python.linting.enabled": True,
        "python.linting.flake8Enabled": True,
        "[yaml]": {"editor.insertSpaces": True, "editor.tabSize": 2},
    }

    os.makedirs(os.path.join(os.sep, THIS_PROJECT, ".vscode"), exist_ok=True)
    settings_path = os.path.join(os.sep, THIS_PROJECT, ".vscode", "settings.json")
    with open(settings_path, "w") as f:
        f.write(json.dumps(template, indent=4))


def start():
    banner = "Beginning CMU-85797 Warehouse setup..."
    one = "Please make sure you have downloaded the source data ZIP file and placed in the `source_data` folder of this project"
    uv = "You also need to install `uv` in order to continue. Refer to the README.md for more details"
    two = "This script will set up an environment on your computer so you can run the project"
    three = "Refer to the `README.md` after this process completes."
    directions = [one, uv, two, three]
    max_len = max(len(line) for line in directions)
    border = "=" * (max_len + 4)
    buffer = ["", ""]
    print("\n" + border)
    _msg([banner, "", *directions], max_len)
    _env()
    _msg(["Setting up environment... this might take a minute", *buffer], max_len)
    _setup_env()
    _msg([*buffer, "Installations complete!"], max_len)

    _msg([*buffer, "Configuring VSCode settings..."], max_len)
    _settings_json()
    complete = [
        "Setup complete.",
        "You can start development on your Warehouse project. Please refer to the README.md to get started",
    ]
    _msg(complete, max_len)
    print(border + "\n")


if __name__ == "__main__":
    start()
