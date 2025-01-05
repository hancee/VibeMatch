import re
from functools import partial


def findone_by_pattern(pattern, str_):
    is_matched = re.search(pattern, str_)
    if is_matched:
        return is_matched.group(1)
    else:
        return None


get_brand = partial(findone_by_pattern, r"\[(.*?)\]")
get_name = partial(findone_by_pattern, r"\] (.*)")
