from pathlib import Path
import pandas as pd


# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Path to environmental dataset
DATASET_PATH = PROJECT_ROOT / "data" / "environmental_metrics.csv"


def load_environmental_data():
    """
    Load environmental metrics from the CSV dataset.
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Environmental dataset not found at: {DATASET_PATH}"
        )

    data = pd.read_csv(DATASET_PATH)

    return data


def get_location(location_id):
    """
    Retrieve environmental information for a specific location.
    """

    data = load_environmental_data()

    location = data[data["location_id"] == location_id]

    if location.empty:
        return None

    return location.iloc[0].to_dict()


if __name__ == "__main__":
    data = load_environmental_data()

    print("\nEnvironmental Dataset")
    print("---------------------")

    print(f"Number of locations: {len(data)}")

    print("\nAvailable locations:")

    for location_id in data["location_id"]:
        print(f"- {location_id}")

    print("\nExample location:")

    example = get_location("LOC001")

    print(example)