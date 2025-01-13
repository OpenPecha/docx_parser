import os
import re
from pathlib import Path

from bs4 import BeautifulSoup  # type: ignore


def clean_text(text: str) -> str:
    # cleaning the text by removing unwanted characters and spaces
    text = text.replace("\n", " ").replace("\xa0", " ")
    text = re.sub(r"[^\u0F00-\u0FFF]+", "", text)
    return text.strip()


def create_ouput_folder(folder_name: str) -> str:
    # create a new output folder. if it doesnt exist
    os.makedirs(folder_name, exist_ok=True)
    return folder_name


def extract_title(span_tag) -> str:
    # Extract and clean the title from a <span> with class 'c3' or 'c35'
    span_class = span_tag.get("class", [])
    if "c3" in span_class or "c35" in span_class:
        raw_title = span_tag.get_text(strip=True)
        # remove number and dot from the title
        return re.sub(r"^\d+\.\s*", "", raw_title)
    return None


def extract_content(span_tag) -> list:
    # extract and clean the content from <span> tag with class c1 or c24
    content = []
    span_class = span_tag.get("class", [])
    if "c1" in span_class or "c24" in span_class:
        raw_content = span_tag.get_text(strip=True)
        cleaned_content = clean_text(raw_content)
        if cleaned_content:
            content.append(cleaned_content)
    return content


def save_content_to_file(
    title: str, content: list, file_counter: int, output_folder: Path
):
    # writes or saves the title and content to a text file.
    sanitized_title = f"{file_counter: 04d}"  # 0001.txt 0002.txt ...
    file_path = output_folder / f"{sanitized_title}.txt"
    file_content = f"{title}\n{'\n'.join(content)}\n"
    file_path.write_text(file_content, encoding="utf-8")


def process_file(file_path: Path, output_folder: Path):
    # Process the XHTML file and extract titles and content.

    xhtml_content = file_path.read_text(encoding="utf-8")

    soup = BeautifulSoup(xhtml_content, "html.parser")
    body = soup.find("body")
    if not body:
        print("No <body> tag found")
        return

    current_title = None
    current_content = []
    file_counter = 1
    skip_next = False

    span_tags = body.find_all("span")
    for span_walker, span_tag in enumerate(span_tags):

        # Skip or ignore empty span tags
        if skip_next:
            skip_next = False
            continue

        if not span_tag.get_text(strip=True):
            continue

        title = extract_title(span_tag)
        if title:
            if current_title and current_content:
                save_content_to_file(
                    current_title, current_content, file_counter, output_folder
                )
                file_counter += 1
            current_title = title
            current_content = []
        else:
            content = extract_content(span_tag)
            if content:
                if "c24" in span_tag.get("class", []):
                    # Merge with preceding and following content
                    prev_content = current_content.pop() if current_content else ""
                    next_content = (
                        extract_content(span_tags[span_walker + 1])
                        if span_walker + 1 < len(span_tags)
                        else []
                    )
                    merged_content = (
                        f"{prev_content} {content[0]} {' '.join(next_content)}".strip()
                    )
                    # Replace the next content with the merged version
                    current_content.append(merged_content)
                    # if the following span have c1 class then skip that content for the continuation.
                    if span_walker + 1 < len(span_tags) and "c1" in span_tags[
                        span_walker + 1
                    ].get("class", []):
                        skip_next = True
                else:
                    current_content.extend(content)

    if current_title and current_content:
        save_content_to_file(
            current_title, current_content, file_counter, output_folder
        )

    print(f"Extracted content has been saved in the '{output_folder}' folder.")


def main():
    # get the path to file

    docx_xhtml_path = Path("./data/transcript_doc.xhtml")
    output_folder = Path("./data/extracted_files")
    create_ouput_folder(output_folder)
    process_file(docx_xhtml_path, output_folder)


if __name__ == "__main__":
    main()
