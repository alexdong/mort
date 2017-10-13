import os
import subprocess

from mort.local_conf import SOURCE_CODE_PATH


def get_git_hash(path: str = SOURCE_CODE_PATH) -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=path).strip().decode('utf-8')


def create_dir_if_not_exists(path: str) -> bool:
    if os.path.exists(path):
        return False

    os.makedirs(path)
    return True


def get_absolute_path(relative_path):
    """ Pycharm test environment differs from py.test. So here we
    try to accomodate both by making a slight change to the path.

    All the `relative_path` assume it's in the project's root directory,
    whereas Pycharm considers the `getcwd` to be in `tests`. """
    cwd = os.getcwd()
    if cwd.endswith('tests'): # pragma: no cover
        cwd = cwd.replace('/tests', '')
    return os.path.join(cwd, relative_path)