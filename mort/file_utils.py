import os
import subprocess

from mort.local_conf import SOURCE_CODE_PATH


def get_git_hash(path: str = SOURCE_CODE_PATH) -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=path).strip().decode('utf-8')


def create_dir_if_not_exists(path: str) -> bool:
    if os.path.exists(path):
        return False
    else:
        os.makedirs(path)
        return True
