from src.assets import perfume_ids, perfume_id_alias_map
from src.utils.flanker_detector import is_flanker
import numpy as np
import pandas as pd
from src.utils.definitions import ASSETS_DIRECTORY
from pathlib import Path
import os

# Load dataframes
pretty_df = pd.read_pickle(Path.joinpath(ASSETS_DIRECTORY, "pretty_df.pkl"))
if os.exists(Path.joinpath(ASSETS_DIRECTORY, "cos_sim_matrix.npy")):
    cos_sim_matrix = np.load(Path.joinpath(ASSETS_DIRECTORY, "cos_sim_matrix.npy"))
else:
    # Download from Google Drive
    import requests

    file_id = "1cUxPg4hvJni5ZgQnncnCJwLUPcQQt-4L"
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url)
    if response.status_code == 200:
        # Save the downloaded file locally
        with open(Path.joinpath(ASSETS_DIRECTORY, "cos_sim_matrix.npy"), "wb") as f:
            f.write(response.content)
        # Load the numpy array
        cos_sim_matrix = np.load(Path.joinpath(ASSETS_DIRECTORY, "cos_sim_matrix.npy"))
    else:
        raise Exception("Failed to download file from Google Drive.")


class AccordBasedRecommender:
    def __init__(self):
        self.cos_sim_matrix = cos_sim_matrix
        self.pretty_df = pretty_df

    def get_flanker_idxs(self, perfume_alias):
        return [
            list(perfume_id_alias_map.values()).index(alias)
            for alias in perfume_id_alias_map.values()
            if (is_flanker(perfume_alias, alias)) & (alias != perfume_alias)
        ]

    def remove_flankers_from_cos_sim_matrix(self, flanker_idxs):
        cos_sim_matrix_ = self.cos_sim_matrix.copy()
        cos_sim_matrix_[flanker_idxs, :] = 0
        cos_sim_matrix_[:, flanker_idxs] = 0
        return cos_sim_matrix_

    def recommend_perfumes(self, perfume_id, n=5, remove_flankers=False):
        """
        Recommend similar perfumes based on a given perfume using cosine similarity.

        :param perfume_id: The id of the query perfume.
        :param n: Number of recommendations to return.
        :param remove_flankers: Whether to exclude flankers from the recommendations.
        :return: DataFrame of recommended perfumes.
        """
        if perfume_id not in perfume_ids:
            raise ValueError(f"{perfume_id} not found in dataset.")

        perfume_id_idx = perfume_ids.index(perfume_id)
        perfume_alias = perfume_id_alias_map[perfume_id]

        flanker_idxs = []
        if remove_flankers:
            flanker_idxs = self.get_flanker_idxs(perfume_alias)

        cos_sim_matrix = (
            self.remove_flankers_from_cos_sim_matrix(flanker_idxs)
            if remove_flankers
            else self.cos_sim_matrix
        )

        # Get similarity scores for the perfume
        similarity_scores = cos_sim_matrix[perfume_id_idx]

        # Sort by similarity, exclude the query perfume itself
        similar_indices = np.argsort(similarity_scores)[::-1][1 : n + 1]

        # Map indices to perfume names
        recommendations = [perfume_ids[i] for i in similar_indices]
        output_ = pretty_df.loc[recommendations]

        return output_


accord_based_recommender = AccordBasedRecommender()
