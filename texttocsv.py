import csv
import re

# -------- CONFIG --------
INPUT_FILE = "input.txt"     # paste your Nepali text here
OUTPUT_FILE = "voter_data.csv"

# Nepali digit regex
NEPALI_NUMBER = re.compile(r"^[०-९]+$")

def is_nepali_number(text):
    return bool(NEPALI_NUMBER.match(text.strip()))

# -------- READ FILE --------
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

records = []
i = 0

while i < len(lines):
    # 1️⃣ Serial number
    if not is_nepali_number(lines[i]):
        i += 1
        continue

    serial_no = lines[i]
    voter_no = lines[i + 1]
    i += 2

    # 2️⃣ Name (can be multi-line)
    name_parts = []
    while i < len(lines) and not is_nepali_number(lines[i]):
        if lines[i] in ["महिला", "पुरुष"]:
            break
        name_parts.append(lines[i])
        i += 1
    name = " ".join(name_parts)

    # 3️⃣ Age
    age = lines[i]
    i += 1

    # 4️⃣ Gender
    gender = lines[i]
    i += 1

    # 5️⃣ Parent/Spouse (can be multi-line)
    parent_parts = []
    while i < len(lines) and not is_nepali_number(lines[i]):
        parent_parts.append(lines[i])
        i += 1
    parent = " ".join(parent_parts)

    records.append([
        serial_no,
        voter_no,
        name,
        age,
        gender,
        parent
    ])

# -------- WRITE CSV --------
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([
        "सि.नं",
        "मतदाता नं",
        "नाम",
        "उमेर",
        "लिङ्ग",
        "पति/पिता/माता"
    ])
    writer.writerows(records)

print("✅ CSV file created successfully:", OUTPUT_FILE)
