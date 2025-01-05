import pandas as pd
from src.utils.note_based_recommender import (
    get_neighbors_by_perfume_id,
    get_neighbors_by_note_list,
)
from src.utils.accord_based_recommender import accord_based_recommender


def get_perfumes_with_similar_notes_based_on_perfume_id(
    perfume_id: str,
) -> pd.DataFrame:
    return get_neighbors_by_perfume_id(perfume_id=perfume_id)


def get_perfumes_with_similar_notes_based_on_note_list(
    note_list: list,
) -> pd.DataFrame:
    # Note: Not yet integrated, requires additional agent to minimize confusion.
    return get_neighbors_by_note_list(note_list=note_list)


def get_perfumes_with_similar_accords_based_on_perfume_id(
    perfume_id, n=5, remove_flankers=False
) -> pd.DataFrame:
    return accord_based_recommender.recommend_perfumes(
        perfume_id=perfume_id, n=n, remove_flankers=remove_flankers
    )


def get_perfumes_x_flankers_with_similar_accords_based_on_perfume_id(
    perfume_id, n=5, remove_flankers=True
) -> pd.DataFrame:
    """Exclude flankers from recommendations"""
    return accord_based_recommender.recommend_perfumes(
        perfume_id=perfume_id, n=n, remove_flankers=remove_flankers
    )
