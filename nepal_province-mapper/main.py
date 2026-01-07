import pandas as pd
from rapidfuzz import process

# =========================
# 1️⃣ District → Province mapping
# =========================

district_to_province = {
    # Koshi
    "taplejung": "Koshi", "panchthar": "Koshi", "ilam": "Koshi", "jhapa": "Koshi",
    "morang": "Koshi", "sunsari": "Koshi", "dhankuta": "Koshi", "terhathum": "Koshi",
    "sankhuwasabha": "Koshi", "bhojpur": "Koshi", "solukhumbu": "Koshi",
    "okhaldhunga": "Koshi", "khotang": "Koshi", "udayapur": "Koshi",

    # Madhesh
    "saptari": "Madhesh", "siraha": "Madhesh", "dhanusha": "Madhesh",
    "mahottari": "Madhesh", "sarlahi": "Madhesh", "rautahat": "Madhesh",
    "bara": "Madhesh", "parsa": "Madhesh",

    # Bagmati
    "dolakha": "Bagmati", "ramechhap": "Bagmati", "sindhuli": "Bagmati",
    "kavrepalanchok": "Bagmati", "sindhupalchok": "Bagmati",
    "bhaktapur": "Bagmati", "lalitpur": "Bagmati", "kathmandu": "Bagmati",
    "nuwakot": "Bagmati", "dhading": "Bagmati", "rasuwa": "Bagmati",
    "makwanpur": "Bagmati", "chitwan": "Bagmati",

    # Gandaki
    "gorkha": "Gandaki", "lamjung": "Gandaki", "tanahun": "Gandaki",
    "kaski": "Gandaki", "manang": "Gandaki", "mustang": "Gandaki",
    "myagdi": "Gandaki", "parbat": "Gandaki", "baglung": "Gandaki",
    "syangja": "Gandaki", "nawalpur": "Gandaki",

    # Lumbini
    "rupandehi": "Lumbini", "kapilvastu": "Lumbini", "palpa": "Lumbini",
    "gulmi": "Lumbini", "arghakhanchi": "Lumbini", "dang": "Lumbini",
    "banke": "Lumbini", "bardiya": "Lumbini", "pyuthan": "Lumbini",
    "rolpa": "Lumbini", "rukum east": "Lumbini",

    # Karnali
    "dolpa": "Karnali", "jumla": "Karnali", "kalikot": "Karnali",
    "mugu": "Karnali", "humla": "Karnali", "jajarkot": "Karnali",
    "dailekh": "Karnali", "salyan": "Karnali",
    "rukum west": "Karnali", "surkhet": "Karnali",

    # Sudurpashchim
    "bajura": "Sudurpashchim", "bajhang": "Sudurpashchim",
    "darchula": "Sudurpashchim", "baitadi": "Sudurpashchim",
    "dadeldhura": "Sudurpashchim", "doti": "Sudurpashchim",
    "achham": "Sudurpashchim", "kailali": "Sudurpashchim",
    "kanchanpur": "Sudurpashchim",
}

district_list = list(district_to_province.keys())

# Nepali → English mapping
nepali_to_english = {
    "काठमाण्डौ": "kathmandu",
    "भक्तपुर": "bhaktapur",
    "ललितपुर": "lalitpur",
    "रुपन्देही": "rupandehi",
    "चितवन": "chitwan",
    "काभ्रेपलाञ्चोक": "kavrepalanchok",
    # add more as needed
}

# =========================
# 2️⃣ Helper functions
# =========================

def normalize_text(text):
    if pd.isna(text):
        return ""
    return str(text).lower().strip()

def find_province_from_address(address):
    # Convert NaN to empty string
    if pd.isna(address):
        address = ""
    
    # Normalize English
    address_norm = normalize_text(address)

    # 1️⃣ Check English districts directly
    for d in district_list:
        if d in address_norm:
            return district_to_province[d]

    # 2️⃣ Fuzzy match (English)
    if address_norm:  # only if string is not empty
        match, score, _ = process.extractOne(address_norm, district_list)
        if score >= 85:
            return district_to_province[match]

    # 3️⃣ Check Nepali districts
    for nep, eng in nepali_to_english.items():
        if nep in str(address):  # convert to string just in case
            return district_to_province.get(eng, "Unknown")

    return "Unknown"

# =========================
# 3️⃣ Load CSV
# =========================

df = pd.read_csv("data5.csv")

# =========================
# 4️⃣ Apply mapping
# =========================

df["province"] = df["Address"].apply(find_province_from_address)

# =========================
# 5️⃣ Save output
# =========================

df.to_csv("data5_with_province.csv", index=False)

print("✅ Province mapping completed. File saved as data5_with_province.csv")
