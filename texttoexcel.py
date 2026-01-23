import pandas as pd

# Read the raw data from a text file
with open("voters.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]  # Remove empty lines

# Prepare lists
voters = []
temp = []

for line in lines:
    # Check if the line is a serial number (purely numeric, usually 1-3 digits)
    if line.isdigit() and (len(temp) > 0):
        voters.append(temp)
        temp = [line]
    else:
        temp.append(line)

# Append the last voter
if temp:
    voters.append(temp)

# Now, map the data into columns
columns = ["सि.नं.", "मतदाता नं", "मतदाताको नाम", "उमेर", "लिङ्ग", "पति/पत्नीको नाम", "पिता / माताको नाम"]
structured_data = []

for voter in voters:
    # Initialize fields
    serial, voter_id, name, age, gender, spouse, parent = ([""] * 7)
    
    try:
        serial = voter[0]
        voter_id = voter[1]
        name = voter[2]
        age = voter[3] if len(voter) > 3 else ""
        gender = voter[4] if len(voter) > 4 else ""
        
        # Remaining lines may contain spouse/parent info
        remaining = voter[5:] if len(voter) > 5 else []
        
        if len(remaining) == 1:
            spouse = remaining[0]
        elif len(remaining) >= 2:
            spouse = remaining[0]
            parent = " / ".join(remaining[1:])

    except IndexError:
        pass

    structured_data.append([serial, voter_id, name, age, gender, spouse, parent])

# Create DataFrame
df = pd.DataFrame(structured_data, columns=columns)

# Save to Excel
df.to_excel("voters_clean.xlsx", index=False)
print("✅ Excel file 'voters_clean.xlsx' created successfully!")
