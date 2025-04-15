#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Realtek Semiconductor Corp.
# SPDX-License-Identifier: Apache-2.0 

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

from scripts.base.Const import *
from scripts.base.EnvUtils import run_command, is_repo_workspace, is_git_workspace

CMD_CLEAN_GIT_WORKSPACE = "git reset --hard && git clean -fd"
CMD_GIT_UPDATE = 'git pull'
CMD_REPO_UPDATE = 'repo sync'
CMD_REPO_LIST = "repo list | awk '{print $1}'"
CMD_INSTALL_LOONG_REQUIREMENTS = 'pip install -r ' + LOONG_SDK_PIP_REQUIREMENTS_PATH
CMD_CLEAN_WORKSPACE = "repo forall -c 'git reset --hard && git clean -fd'"
CMD_RM_PRE_COMMIT_HOOKS = 'find .repo/ -name "pre-commit" | grep -v ".repo/repo/hooks/" | xargs rm'
CMD_RM_COMMIT_MSG_HOOKS = 'find .repo/ -name "commit-msg" | grep -v ".repo/repo/hooks/" | xargs rm'

GIT_HOOKS_SYNC_FAIL_MSG = 'Not replacing locally modified'


def update_git_hooks():
    if os.path.exists(LOONG_SDK_GIT_HOOKS_TGT_DIR):
        hooks = glob.glob(LOONG_SDK_GIT_HOOKS_SRC_DIR + '/*')
        for hook in hooks:
            if os.path.isdir(hook):
                pass
            elif os.path.isfile(hook):
                shutil.copy(hook, LOONG_SDK_GIT_HOOKS_TGT_DIR)
                os.system("chmod a+x " + os.path.join(LOONG_SDK_GIT_HOOKS_TGT_DIR, os.path.basename(hook)))
            else:
                pass
    else:
        print('Error: Repo damaged, no hooks directory found')
        sys.exit(2)

    print('Sync Git hooks to repositories...')
    rc = run_command(CMD_REPO_UPDATE + ' 2>&1', True)
    if rc.returncode != 0:
        print('Error: Fail to sync Git hooks to repositories')
        sys.exit(2)
    elif GIT_HOOKS_SYNC_FAIL_MSG in rc.stdout:
        print('Warning: Fail to sync Git hooks, retry')
        run_command(CMD_RM_PRE_COMMIT_HOOKS, True)
        run_command(CMD_RM_COMMIT_MSG_HOOKS, True)
        rc = run_command(CMD_REPO_UPDATE + ' 2>&1')
        if rc.returncode != 0:
            print('Error: Fail to sync Git hooks to repositories')
            print(rc.stdout)
            sys.exit(2)
        else:
            pass
    else:
        pass


def check_venv():
    print("Check Python virtual environment...")
    if os.path.exists(LOONG_SDK_VENV_DIR):
        print("Python virtual environment exists")
    else:
        # Create virtual environment if it does not exist
        try:
            print("Python virtual environment does not exist")
            import venv
            venv.create(LOONG_SDK_VENV_DIR)
            print("Python virtual environment created")
        except:
            print("Error: Fail to create Python virtual environment")
            sys.exit(2)


def main(argc, argv):
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('-g', '--update-git-hooks', action='store_true', help='update git hooks')
    parser.add_argument('-p', '--pristine', action='store_true', help='pristine build')
    parser.add_argument('-v', '--venv', action='store_true', help='process in Python virtual enviroment')

    args = parser.parse_args()

    print("Set up...")
    no_vcs_flag = not is_repo_workspace() and not is_git_workspace()
    if args.pristine:
        print("Clean workspace...")
        if is_repo_workspace():
            os.system(CMD_CLEAN_WORKSPACE)
        elif is_git_workspace():
            os.system(CMD_CLEAN_GIT_WORKSPACE)
        else:
            print("Warning: No VCS detected, the 'pristine' argument will be ignored.")
        print("Clean workspace done")
    else:
        pass

    # Check virtual environment
    venv = False
    if args.venv:
        venv = True
        check_venv()
    else:
        pass

    # Update workspace
    workspace_update_return_code = 0
    if no_vcs_flag:
        print('Warning: workspace update will be skipped because no VCS was detected.')
    else:
        print('Update workspace...')
        result = run_command(CMD_REPO_UPDATE if is_repo_workspace() else CMD_GIT_UPDATE, use_venv=venv)
        workspace_update_return_code = result.returncode
        if result.returncode != 0:
            print('Error: Fail to update workspace')
        else:
            print('Update workspace done')

    # Install Python requirements
    print('Install Python requirements...')
    pip_install_result = run_command(CMD_INSTALL_LOONG_REQUIREMENTS, use_venv=venv)
    print('Install Python requirements done')

    if workspace_update_return_code != 0 or pip_install_result.returncode != 0:
        print(f"Error: Set up Loong SDK failed ({workspace_update_return_code}) ({pip_install_result.returncode})")
        sys.exit(2)
    else:
        pass

    if args.update_git_hooks and is_repo_workspace():
        print("Update Git hooks...")
        update_git_hooks()
        print("Update Git hooks done")
    else:
        pass

    print("Set up Loong SDK done")


if __name__ == '__main__':
    main(len(sys.argv), sys.argv[1:])
