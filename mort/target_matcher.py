import json
from typing import Dict, List

from mort.local_conf import TARGET_LIST_FILE_PATH


def matches(target: Dict, pattern: Dict) -> bool:
    """
    Whether the `target` matches the `pattern`, which means that

    * all the keys in `pattern` should also exists in `target`
    * the value for the patterns can also be found in the target.

    All matches are case insensitive.

    :param target: A `target` unit
    :param pattern: The matching pattern
    :return: True if the target matches the pattern
    """
    if not set(pattern.keys()).issubset(set(target.keys())):
        return False
    for (key, substr) in pattern.items():
        if not target[key] or substr.lower() not in target[key].lower():
            return False
    return True


def get_targets(pattern: Dict) -> List[Dict]:
    """
    Return all the targets that matches the pattern from the local target list.

    :param pattern: A matching pattern
    :param from_file: Location to the target list file we are loading all the targets from
    :return: List of all targets
    """
    return [target for target in json.loads(open(TARGET_LIST_FILE_PATH).read()) if matches(target, pattern)]
