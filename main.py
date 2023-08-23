import csv
from docx import Document


def save_to_csv(data, output_file_path):
    with open(output_file_path, "w", encoding="utf-8", newline="") as output_file:
        csv_writer = csv.writer(output_file)
        # csv_writer.writerow(["Text", "Translation"])  # Write header
        csv_writer.writerows(data)


def convert_txt_to_csv(input_file_path, output_file_path):
    data = []

    with open(input_file_path, "r", encoding="utf-8") as input_file:
        blocks = input_file.read().split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) == 2:
            text, translation = lines
            data.append([text.strip(), translation.strip()])

    save_to_csv(data, output_file_path)
    print(f"Conversion complete. Output CSV file: {output_file_path}")


def convert_docx_to_csv(input_file_path, output_file_path):
    doc = Document(input_file_path)
    data = []

    text = ""
    for paragraph in doc.paragraphs:
        content = paragraph.text.strip()

        if not text:
            text = content
        else:
            data.append([text, content])
            text = ""

    save_to_csv(data, output_file_path)
    print(f"Conversion complete. Output CSV file: {output_file_path}")


if __name__ == "__main__":
    convert_docx_to_csv("input.docx", "output.csv")
    # convert_txt_to_csv("input.txt", "output.csv")
