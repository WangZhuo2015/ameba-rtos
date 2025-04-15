import subprocess
import os

from scripts.base.Const import *


def run_command(command, capture_output=False, use_venv=False, venv_path=LOONG_SDK_VENV_DIR):
    if venv_path is None:
        venv_path = os.getenv('LOONG_SDK_VENV_DIR', '.')

    if use_venv:
        if os.name == 'nt':
            # Windows 环境使用 activate.bat
            activate_command = os.path.join(venv_path, 'Scripts', 'activate.bat')
            full_command = f'cmd /c "{activate_command} && {command}"'
        else:
            # 类 Unix 使用 source
            activate_command = os.path.join(venv_path, 'bin', 'activate')
            full_command = f'bash -c "source {activate_command} && {command}"'
    else:
        full_command = command

    # 执行命令
    result = subprocess.run(full_command, shell=True, capture_output=capture_output, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    return result


def is_repo_workspace():
    return os.path.exists('.repo') and os.path.isdir('.repo')


def is_git_workspace():
    return os.path.exists('.git') and os.path.isdir('.git')
