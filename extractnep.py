# # import cv2
# # import pytesseract
# # import pandas as pd

# # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # image = cv2.imread("Screenshot1.png")
# # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

# # text = pytesseract.image_to_string(gray, lang="nep", config="--psm 6")

# # lines = [l.strip() for l in text.split("\n") if l.strip()]
# # rows = []

# # for line in lines:
# #     tokens = line.split()

# #     if len(tokens) < 5:
# #         continue

# #     serial = tokens[0]
# #     voter_id = tokens[1]

# #     if "महिला" in tokens:
# #         gender_index = tokens.index("महिला")
# #         gender = "महिला"
# #     elif "पुरुष" in tokens:
# #         gender_index = tokens.index("पुरुष")
# #         gender = "पुरुष"
# #     else:
# #         continue

# #     name = " ".join(tokens[2:gender_index-1])
# #     age = tokens[gender_index-1]
# #     relation = " ".join(tokens[gender_index+1:])

# #     rows.append({
        # "सि.नं": serial,
        # "मतदाता नं": voter_id,
        # "नाम": name,
        # "उमेर": age,
        # "लिङ्ग": gender,
        # "पति/पिता/माता": relation
# #     })

# # df = pd.DataFrame(rows)
# # df.to_csv("output.csv", index=False, encoding="utf-8-sig")

# # print("✅ Extracted rows:", len(df))
# # print("✅ output.csv created successfully")


# import cv2
# import pytesseract
# import pandas as pd

# # ===============================
# # CONFIG
# # ===============================

# IMAGE_PATH = "Screenshot1.png"   # your image
# OUTPUT_CSV = "output.csv" # final csv

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # ===============================
# # LOAD IMAGE
# # ===============================

# img = cv2.imread(IMAGE_PATH)

# if img is None:
#     raise Exception("❌ Image not found. Make sure image.png is in the same folder.")

# # ===============================
# # PREPROCESS (SAFE)
# # ===============================

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# gray = cv2.adaptiveThreshold(
#     gray,
#     255,
#     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#     cv2.THRESH_BINARY,
#     31,
#     2
# )

# # ===============================
# # OCR (NEPALI)
# # ===============================

# text = pytesseract.image_to_string(
#     gray,
#     lang="nep",
#     config="--psm 6"
# )

# # ===============================
# # GUARANTEED OUTPUT
# # ===============================

# lines = [line.strip() for line in text.split("\n") if line.strip()]

# if len(lines) == 0:
#     raise Exception("❌ OCR returned no text. Check image quality.")

# # ===============================
# # SAVE RAW OCR TO CSV
# # ===============================

# df = pd.DataFrame({"OCR_TEXT": lines})
# df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

# print("✅ OCR SUCCESS")
# print("✅ Lines extracted:", len(lines))
# print("✅ CSV saved as:", OUTPUT_CSV)


import cv2
import pytesseract
import pandas as pd

# ===============================
# CONFIG
# ===============================

IMAGE_PATH = "testshot.png"
OUTPUT_CSV = "output_with_serial1.csv"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ===============================
# LOAD & PREPROCESS IMAGE
# ===============================

img = cv2.imread(IMAGE_PATH)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 31, 2
)

# ===============================
# OCR
# ===============================

text = pytesseract.image_to_string(gray, lang="nep", config="--psm 6")

lines = [l.strip() for l in text.split("\n") if l.strip()]

# ===============================
# GENERATE CLEAN SERIAL NUMBERS
# ===============================

rows = []
serial = 1

for line in lines:
    rows.append({
        "सि.नं": serial,
        "OCR_TEXT": line
    })
    serial += 1

# ===============================
# SAVE CSV
# ===============================

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print("✅ Done")
print("✅ Rows:", len(df))
print("✅ Saved:", OUTPUT_CSV)

