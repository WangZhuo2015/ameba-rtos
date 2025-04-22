#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2025 Realtek Semiconductor Corp.
# SPDX-License-Identifier: Apache-2.0 

import os


LOONG_SDK_VENV_DIR = '.venv'
LOONG_SDK_TOOLCHAIN_DEFAULT_PATH_WINDOWS = 'C:\\msys64\\opt\\rtk-toolchain'
LOONG_SDK_TOOLCHAIN_DEFAULT_PATH_LINUX = '/opt/rtk-toolchain'
LOONG_SDK_PIP_REQUIREMENTS_PATH = 'tools/requirements.txt'
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
CMD_INSTALL_LOONG_REQUIREMENTS = 'python -m pip install -r ' + LOONG_SDK_PIP_REQUIREMENTS_PATH
LOONG_SDK_QUERY_CFG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'query.json')
LOONG_SDK_DEFAULT_IMAGE_DIR = 'images'
LOONG_SDK_DEFAULT_BUILD_DIR = 'build'
LOONG_SDK_BRIEF_DESC = 'Realtek Loong FreeRTOS SDK'
LOONG_SDK_MANIFEST_FILE = os.path.join('.repo', 'manifest.xml')
LOONG_SDK_APP_FILE = 'main.c'
CMD_GET_MANIFEST_URL = "cat .repo/manifests.git/config | grep -m 1 url | cut -d\"=\" -f 2"
LOONG_CONFIG_SCRIPTS_DIR = 'menuconfig'