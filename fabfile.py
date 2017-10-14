# pylint: skip-file

import os

from fabric.api import local


CURRENT_PATH = os.path.dirname(__file__)


def coverage():
    local('pytest --cov=./ --cov-report=term-missing')

def lint():
    local('pylint mort')
    local('mypy --strict-optional --ignore-missing-imports --python-version 3.6 mort tests')
