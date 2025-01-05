from rapidfuzz import fuzz
from src.utils.alias_parser import get_name, get_brand

FLANKER_THRESHOLD = 60


def _custom_prefix_similarity(str_1, str_2):
    """
    Prioritize similarity of the first half (based on longer) of two strings.
    """
    comparison_len = int(max([len(str_1), len(str_2)]) / 2)
    return fuzz.ratio(str_1[:comparison_len], str_2[:comparison_len])


def is_flanker(alias_1, alias_2):
    brand_1, brand_2 = get_brand(alias_1), get_brand(alias_2)
    if brand_1 != brand_2:
        return False
    else:
        name_1, name_2 = get_name(alias_1), get_name(alias_2)
        return _custom_prefix_similarity(name_1, name_2) > FLANKER_THRESHOLD
