import pickle
from pathlib import Path
from src.utils.definitions import ASSETS_DIRECTORY
from src.assets import top_notes
import pandas as pd

# Load dataframes
pretty_df = pd.read_pickle(Path.joinpath(ASSETS_DIRECTORY, "pretty_df.pkl"))
X = pd.read_pickle(Path.joinpath(ASSETS_DIRECTORY, "knn_train_data.pkl"))

# Load the model
knn_model_path = Path.joinpath(ASSETS_DIRECTORY, "knn_model.pkl")
with open(knn_model_path, "rb") as f:
    knn = pickle.load(f)


def get_note_rank(x, note):
    try:
        return len(top_notes) - x.index(note)
    except:
        return -1


def get_neighbors(arr):
    distances, indices = knn.kneighbors([arr])
    reco_perfume_ids = X.iloc[indices[0],].index.tolist()
    return pretty_df.loc[reco_perfume_ids, :]


def get_neighbors_by_note_list(note_list):
    arr = [get_note_rank(note_list, note) for note in top_notes]
    return get_neighbors(arr)


def get_neighbors_by_perfume_id(perfume_id):
    arr = X.loc[perfume_id].values.tolist()
    return get_neighbors(arr)
