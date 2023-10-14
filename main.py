import csv
from docx import Document
import pandas as pd


def save_to_csv(data: list[tuple[str]], output_file_path: str):
    with open(output_file_path, "w", encoding="utf-8", newline="") as output_file:
        csv_writer = csv.writer(output_file)
        # csv_writer.writerow(["Text", "Translation"])  # Write header
        csv_writer.writerows(data)


def get_anki_deck_data(input_file_path: str):
    anki_data = []

    with open(input_file_path, "r", encoding="utf-8") as input_file:
        lines = input_file.readlines()
        for line in lines:
            word1, word2 = line.strip().split("\t")

            if "&#x27;" in word1:
                word1 = word1.replace("&#x27;", "'")
            if "&#x27;" in word2:
                word2 = word2.replace("&#x27;", "'")

            anki_data.append((word1, word2))

    return anki_data


def get_anki_csv_or_excel_data(file_path: str):
    anki_csv_or_excel_data = []
    df = None

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    for index, row in df.iterrows():
        column_c = df.columns[2]  # Adjust column indices as needed
        column_d = df.columns[3]  # Adjust column indices as needed
        anki_csv_or_excel_data.append((row[column_c], row[column_d]))

    print(anki_csv_or_excel_data)
    return anki_csv_or_excel_data


def convert_iflash_txt_to_csv(input_file_path: str, output_file_path: str):
    data = []

    with open(input_file_path, "r", encoding="utf-8") as input_file:
        blocks = input_file.read().split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) == 2:
            text, translation = lines
            data.append((text.strip(), translation.strip()))

    save_to_csv(data, output_file_path)
    print(f"Conversion complete. Output CSV file: {output_file_path}")


def convert_iflash_docx_to_csv(input_file_path: str, output_file_path: str):
    doc = Document(input_file_path)
    data = []

    text = ""
    for paragraph in doc.paragraphs:
        content = paragraph.text.strip()

        if not text:
            text = content
        else:
            data.append((text, content))
            text = ""

    save_to_csv(data, output_file_path)
    print(f"Conversion complete. Output CSV file: {output_file_path}")


if __name__ == "__main__":
    pass
    get_anki_csv_or_excel_data("Saved translations - Portuguese - English.csv")
    # convert_iflash_docx_to_csv("iflash-input.docx", "iflash-output.csv")
    # convert_iflash_txt_to_csv("iflash-input.txt", "iflash-output.csv")
