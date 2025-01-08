import hashlib
import os


def calculate_file_hash(file_path):
    """Calculate the hash of a file to detect duplicates."""
    hash_algo = hashlib.md5()  # Use MD5 for file hashing
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()


def remove_duplicates(folder_path):
    """Remove duplicate files based on their content."""
    seen_hashes = {}
    duplicates = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.endswith((".mp3", ".wav")):
            file_hash = calculate_file_hash(file_path)

            if file_hash in seen_hashes:
                duplicates.append(file_path)
            else:
                seen_hashes[file_hash] = file_path

    # Delete duplicate files
    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Deleted duplicate: {duplicate}")

    print(f"{len(duplicates)} duplicate files removed.")


def process_mp3_files(folder_path):
    """Main function to handle duplicates."""
    if not os.path.exists(folder_path):
        print("The specified folder does not exist.")
        return

    print("Checking and removing duplicates...")
    remove_duplicates(folder_path)


# Folder path where your MP3 files are located
folder_path = input("Enter the folder path: ").strip()
process_mp3_files(folder_path)
