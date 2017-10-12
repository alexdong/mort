import os


def create_dir_if_not_exists(path: str) -> bool:
    if os.path.exists(path):
        return False
    else:
        os.makedirs(path)
        return True
