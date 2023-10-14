import csv
from docx import Document


def save_to_csv(data: list[tuple[str]], output_file_path: str):
    with open(output_file_path, "w", encoding="utf-8", newline="") as output_file:
        csv_writer = csv.writer(output_file)
        # csv_writer.writerow(["Text", "Translation"])  # Write header
        csv_writer.writerows(data)


def convert_iflash_txt_to_csv(input_file_path: str, output_file_path: str):
    data = []

    with open(input_file_path, "r", encoding="utf-8") as input_file:
        blocks = input_file.read().split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) == 2:
            text, translation = lines
            data.append((text.strip(), translation.strip()))

    print(data)
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
    # convert_iflash_docx_to_csv("iflash-input.docx", "iflash-output.csv")
    convert_iflash_txt_to_csv("iflash-input.txt", "iflash-output.csv")
