import csv
import os

FIELDNAMES = ["no", "pertanyaan", "ekspektasi_jawaban", "hasil_teks", "hasil_audio"]

def read_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def write_header(file_path):
    """Menulis header ke file CSV, menimpa file jika sudah ada."""
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

def append_result(file_path, result_row):
    """Menambahkan satu baris hasil ke file CSV."""
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(result_row)
