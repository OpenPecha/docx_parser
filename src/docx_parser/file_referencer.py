import re
from pathlib import Path

import pandas as pd  # type: ignore


def extract_number(filename: str) -> int:
    """
    Extracts the numeric part of a filename to be used for numerical sorting.
    Assumes that the filename starts with a number.
    """
    match = re.match(r"(\d+)", filename)
    return int(match.group(1)) if match else float("inf")


def get_sorted_files(folder: Path) -> list:
    """
    Retrieves and sorts the files in the given folder, excluding '.DS_Store' files.
    Sorts based on the numerical value extracted from the filename.
    """
    return sorted(
        (
            file.name
            for file in folder.iterdir()
            if file.is_file() and file.name != ".DS_Store"
        ),
        key=extract_number,
    )


def create_file_mapping_csv(folder1: Path, folder2: Path, output_csv: Path) -> None:
    """
    Creates a CSV mapping the original and renamed files from two folders.
    The output CSV will be saved at the specified path.
    """
    # Ensure both folders exist
    if not folder1.exists():
        raise FileNotFoundError(f"Folder not found: {folder1}")
    if not folder2.exists():
        raise FileNotFoundError(f"Folder not found: {folder2}")

    # Get sorted filenames from both folders
    original_files = get_sorted_files(folder1)
    renamed_files = get_sorted_files(folder2)

    # Ensure both folders have the same number of files
    if len(original_files) != len(renamed_files):
        raise ValueError("The folders do not contain the same number of files.")

    # Create a DataFrame for the mapping
    df = pd.DataFrame(
        {"Original Filename": original_files, "Renamed Filename": renamed_files}
    )

    # Create the data folder if it doesn't exist
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    # Save the DataFrame to CSV
    df.to_csv(output_csv, index=False)

    print(f"Mapping successfully written to {output_csv}")


def main():
    folder1 = Path("../../data/དབུས་སྐད original extra audio removed")
    folder2 = Path("../../data/དབུས་སྐད Final")
    output_csv = Path("../../data/utsang_reference_experiment.csv")

    # Create and save the mapping
    create_file_mapping_csv(folder1, folder2, output_csv)


if __name__ == "__main__":
    main()
