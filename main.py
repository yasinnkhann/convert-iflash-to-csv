import csv
from docx import Document
import pandas as pd


def save_to_csv(data: list[tuple[str]], output_file_path: str):
    with open(output_file_path, "w", encoding="utf-8", newline="") as output_file:
        csv_writer = csv.writer(output_file)
        # csv_writer.writerow(["Text", "Translation"])  # Write header
        csv_writer.writerows(data)


def get_anki_deck_data(file_path: str):
    anki_data = []

    with open(file_path, "r", encoding="utf-8") as input_file:
        lines = input_file.readlines()
        for line in lines:
            card_set = line.strip().split("\t")
            if len(card_set) == 2:
                word1, word2 = card_set
                if "&#x27;" in word1:
                    word1 = word1.replace("&#x27;", "'")
                if "&#x27;" in word2:
                    word2 = word2.replace("&#x27;", "'")

                anki_data.append((word1, word2))

        return anki_data


def get_google_translate_csv_or_excel_data(file_path: str):
    anki_csv_or_excel_data = []
    df = None

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    for index, row in df.iterrows():
        column_c = df.columns[2]
        column_d = df.columns[3]
        anki_csv_or_excel_data.append((row[column_d], row[column_c]))

    return anki_csv_or_excel_data


def add_new_cards(anki_deck_file_path, google_translate_csv_or_excel_file_path):
    cards_to_write = []
    anki_deck_data = get_anki_deck_data(anki_deck_file_path)
    anki_csv_or_excel_data = get_google_translate_csv_or_excel_data(
        google_translate_csv_or_excel_file_path
    )

    for anki_csv_or_excel_words in anki_csv_or_excel_data:
        if anki_csv_or_excel_words not in anki_deck_data:
            cards_to_write.append(anki_csv_or_excel_words)

    save_to_csv(cards_to_write, "newly-added-french-cards.csv")


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
    add_new_cards("anki-french-deck.txt", "Saved translations - French - English.csv")
    # convert_iflash_docx_to_csv("iflash-input.docx", "iflash-output.csv")
    # convert_iflash_txt_to_csv("iflash-input.txt", "iflash-output.csv")
