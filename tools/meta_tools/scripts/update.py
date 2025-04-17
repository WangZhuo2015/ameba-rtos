#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Realtek Semiconductor Corp.
# SPDX-License-Identifier: Apache-2.0 

import argparse
import glob
import os
import shutil
import subprocess
import sys

from base.EnvUtils import is_repo_workspace, is_git_workspace, run_command

LOONG_SDK_GIT_HOOKS_SRC_DIR = 'tools/meta_tools/git_hooks'
LOONG_SDK_GIT_HOOKS_TGT_DIR = '.repo/repo/hooks'

CMD_CLEAN_GIT_WORKSPACE="git reset --hard && git clean -fd"
CMD_GIT_UPDATE = 'git pull'
CMD_CLEAN_WORKSPACE = "repo forall -c 'git reset --hard && git clean -fd'"
CMD_REPO_UPDATE = 'repo sync'
CMD_REPO_LIST = "repo list | awk '{print $1}'"
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
    rc = run_command(CMD_REPO_UPDATE + ' 2>&1', show_output=True)
    if rc.returncode != 0:
        print('Error: Fail to sync Git hooks to repositories')
        sys.exit(2)
    elif GIT_HOOKS_SYNC_FAIL_MSG in (rc.stdout or ""):
        print('Warning: Fail to sync Git hooks, retry')
        run_command(CMD_RM_PRE_COMMIT_HOOKS, show_output=True)
        run_command(CMD_RM_COMMIT_MSG_HOOKS, show_output=True)
        rc = run_command(CMD_REPO_UPDATE + ' 2>&1', show_output=True)
        if rc.returncode != 0:
            print('Error: Fail to sync Git hooks to repositories')
            print(rc.stdout)
            sys.exit(2)
        else:
            pass
    else:
        pass


def main(argc, argv):
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('-p', '--pristine', action='store_true', help='pristine build')

    args = parser.parse_args()

    no_vcs_flag = not is_repo_workspace() and not is_git_workspace()
    if no_vcs_flag:
        print('Warning: Invalid repo or git workspace, ignored')
        sys.exit(1)
    else:
        pass

    print('Update...')
    if args.pristine:
        print("Clean workspace...")
        if is_repo_workspace():
            os.system(CMD_CLEAN_WORKSPACE)
        elif is_git_workspace():
            os.system(CMD_CLEAN_GIT_WORKSPACE)
        else:
            # Should not reach here, because of the 'no_vcs_flag' check
            print("Warning: No VCS detected, the 'pristine' argument will be ignored.")
        print("Clean workspace done")
    else:
        pass

    print('Update workspace...')
    os.system(CMD_REPO_UPDATE if is_repo_workspace() else CMD_GIT_UPDATE)

    if is_repo_workspace():
        print('Update Git hooks...')
        update_git_hooks()

    print('Update done')


if __name__ == '__main__':
    main(len(sys.argv), sys.argv[1:])
