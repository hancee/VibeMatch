from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).parent.parent.parent.resolve()
DATA_DIRECTORY = Path.joinpath(PROJECT_DIRECTORY, "data")
ASSETS_DIRECTORY = Path.joinpath(PROJECT_DIRECTORY, "src", "assets")
