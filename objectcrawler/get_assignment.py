"""
Module for containing gc introspection function
"""

import gc


def get_assignment(obj) -> str:
    """
    Attempts to extract the assignment location of object `obj` from gc

    :param obj:
        Object to query
    :return:
        assignment location
    """
    locations = []
    for item in gc.get_referrers(obj):
        if isinstance(item, dict):
            for k, v in item.items():
                if v is obj:
                    locations.append(k)
    if len(locations) == 0:
        return "~"
    return locations[0]
