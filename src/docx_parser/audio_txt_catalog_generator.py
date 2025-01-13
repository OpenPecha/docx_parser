# this script is used by taking in already existing csv file and then generates a new csv with catalogue.
# you can modify the code as needed.
# this script is to generate a catalog. mainly for corresponding txt and audio files (.mp3 or .wav)
# Sr no,Original Filename,Renamed Filename,ID,Text Link,Audio Link,Standard Duration (hh:mm:ss)
# you can add extra functions as your needs which resembles the catalog format
# note -> change the output directory, change the input directory and audio files directory,
# change the link names as well

from pathlib import Path

import pandas as pd  # type:ignore
from pydub import AudioSegment  # type:ignore


# Function to generate ID (STT_KAB000X format)
def generate_id(start_index, count):
    return [f"STT_KAB{str(start_index + i).zfill(4)}" for i in range(count)]


# Function to generate Text links
def generate_text_links(start_index, count):
    # ** dont forget to change the name here. naykor_<change_name>_data **
    base_url = (
        "https://s3.ap-south-1.amazonaws.com/monlam.ai.stt/naykor_data/naykor_kham_data"
    )
    return [
        f"{base_url}/STT_NY_{str(start_index + i).zfill(4)}/{str(start_index + i).zfill(4)}.txt"
        for i in range(count)
    ]  # noqa


# Function to generate Audio links
def generate_audio_links(catalog_df, start_index, count):
    # ** dont forget to change the name here. naykor_<change_name>_data **
    extensions = catalog_df["Renamed Filename"].apply(
        lambda x: Path(x).suffix.lstrip(".")
    )  # extract the extension from original filename column
    base_url = (
        "https://s3.ap-south-1.amazonaws.com/monlam.ai.stt/naykor_data/naykor_kham_data"
    )
    return [
        f"{base_url}/STT_NY_{str(start_index + i).zfill(4)}/{str(start_index + i).zfill(4)}.{extensions[i]}"
        for i in range(count)
    ]


def generate_durations(folder_path):
    """Generate durations for audio files in a folder, sorted by numeric filenames.

    Args:
        folder_path (str or Path): Path to the folder containing audio files.

    Returns:
        list: A list of audio durations in 'hh:mm:ss' format.
    """
    folder = Path(folder_path)
    # Get all audio files in the folder, exluding .DS_Store
    audio_files = [file for file in folder.glob("*") if file.name != ".DS_Store"]
    # Sort files by numeric part of their names (before the extension)
    sorted_files = sorted(
        audio_files,
        key=lambda f: int(f.stem),  # Convert file name (before extension) to int
    )

    durations = []

    for file in sorted_files:
        try:
            # Load audio file
            audio = AudioSegment.from_file(file)
            # Get duration in seconds
            duration_seconds = len(audio) / 1000

            # Convert seconds to hh:mm:ss format
            hours = int(duration_seconds // 3600)
            minutes = int((duration_seconds % 3600) // 60)
            seconds = int(duration_seconds % 60)
            duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"  # noqa

            durations.append(duration_str)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            durations.append(
                "00:00:00"
            )  # Placeholder for files that can't be processed

    return durations


# Function to update the existing catalog
def update_catalog(csv_file_path, audio_folder_path, start_index):
    catalog_df = pd.read_csv(csv_file_path)  # working with the existing csv file.
    # Get the number of rows in the DataFrame
    row_count = len(catalog_df)

    # Generate the new columns based on the row count
    catalog_df["ID"] = generate_id(start_index, row_count)
    catalog_df["Text Link"] = generate_text_links(start_index, row_count)
    catalog_df["Audio Link"] = generate_audio_links(catalog_df, start_index, row_count)
    catalog_df["Standard Duration (hh:mm:ss)"] = generate_durations(audio_folder_path)

    # Save the updated DataFrame to a new CSV file
    updated_csv_file_path = "../../data/kham_reference/kham_catalog.csv"  # change it.
    catalog_df.index = catalog_df.index + 1
    catalog_df.to_csv(updated_csv_file_path, index=True, index_label="Sr no")
    print(f"Updated catalog saved to {updated_csv_file_path}")


# Example usage
if __name__ == "__main__":
    # Path to your existing CSV file (i would suggest wrok on duplicate file)
    csv_file_path = "../../data/kham_reference/kham_reference.csv"
    audio_folder_path = "../../data/ཁམས་སྐད Final"  # change it
    start_index = 1
    update_catalog(csv_file_path, audio_folder_path, start_index)
