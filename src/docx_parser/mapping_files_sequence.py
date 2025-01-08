# This script is used to map the extracted files to the proper folder structure. Works properly with the utsang and kham
import os
import shutil

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
folder1 = os.path.join(base_dir, "extracted_files")
folder2 = os.path.join(base_dir, "ཨ་མདོའི་སྐད Final")
output_folder = os.path.join(base_dir, "amdo_naykor_data_experiment")

os.makedirs(output_folder, exist_ok=True)


# Custom function to extract number from filename
def extract_number_from_filename(filename):
    # Remove the file extension
    base_name = os.path.splitext(filename)[0]
    # Extract numbers only from the base filename
    number_str = "".join([char for char in base_name if char.isdigit()])
    return int(number_str) if number_str else float("inf")


def copy_files_sequentially(source_folder):
    # Get the list of files in the folder
    files = sorted(
        (file for file in os.listdir(source_folder) if file != ".DS_Store"),
        key=extract_number_from_filename,
    )

    for idx, file in enumerate(files, start=1):
        # Determine the target folder (e.g., stt_ny_1, stt_ny_2, ...)
        folder_name = f"STT_NY_{idx: 04d}"
        target_folder = os.path.join(
            output_folder, folder_name
        )  # naykor_data -> stt_ny_1, stt_ny_2, ...
        # Ensure the target folder exists
        os.makedirs(target_folder, exist_ok=True)
        # Copy the file into the target folder
        source_path = os.path.join(source_folder, file)
        target_path = os.path.join(target_folder, file)
        shutil.copy(source_path, target_path)


copy_files_sequentially(folder1)
copy_files_sequentially(folder2)
print("File copying completed successfully.")
