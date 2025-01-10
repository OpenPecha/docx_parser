# This script is used to map the extracted files to the proper folder structure. Works properly with the utsang and kham
import shutil
from pathlib import Path


def extract_number_from_filename(filename: Path) -> int:
    """
    here the file name consists of number in it which i am extracting the number part only.
    Extract numbers from the filename. If no numbers are found, return infinity.
    """
    number_str = "".join([char for char in filename.stem if char.isdigit()])
    return int(number_str) if number_str else float("inf")


def copy_files_sequentially(source_folder: Path, output_folder: Path):
    """
    Copy files from the source folder to sequentially named subfolders in the output folder.
    STT_NY_0001 -> 0001.txt,0001.mp3 | STT_NY_0002 -> 0002.txt,0002.wav ....
    """
    # Ensure the output folder exists
    output_folder.mkdir(parents=True, exist_ok=True)

    # Get the sorted list of files
    files = sorted(
        (file for file in source_folder.iterdir() if file.name != ".DS_Store"),
        key=extract_number_from_filename,
    )

    # Copy files into sequentially numbered folders
    for idx, file in enumerate(files, start=1):
        folder_name = f"STT_NY_{idx: 04d}"
        target_folder = output_folder / folder_name
        target_folder.mkdir(parents=True, exist_ok=True)

        target_path = target_folder / file.name
        shutil.copy(file, target_path)
    print(f"Files copied from {source_folder} to {output_folder}")


def main():

    base_dir = Path("../../data")
    folder1 = base_dir / "extracted_files copy for kham"
    folder2 = base_dir / "ཁམས་སྐད Final"
    output_folder = base_dir / "kham_naykor_data2"

    copy_files_sequentially(folder1, output_folder)
    copy_files_sequentially(folder2, output_folder)
    print("File copying completed successfully.")


if __name__ == "__main__":
    main()
