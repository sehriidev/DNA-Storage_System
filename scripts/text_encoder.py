# LOAD TEXT FILE
with open("input_data/sample.txt", "r", encoding="utf-8") as file:
    text_data = file.read()

print("[ok] Text file loaded")

# =========================
# TEXT → BINARY
# =========================

# =========================
# TEXT → BINARY
# =========================

binary_data = ''.join(
    format(byte, '08b')
    for byte in text_data.encode('utf-8')
)

print("[ok] Text converted to binary")

# =========================
# BINARY → DNA
# =========================

dna_map = {
    "00": "A",
    "01": "T",
    "10": "C",
    "11": "G"
}

dna_sequence = ''.join(
    dna_map[binary_data[i:i+2]]
    for i in range(0, len(binary_data), 2)
)

print("[ok] Binary converted to DNA")

# =========================
# SAVE DNA
# =========================

with open("dna_storage/text_dna.txt", "w") as file:
    file.write(dna_sequence)

print("[ok] DNA saved")

print("\n[success] TEXT ENCODING COMPLETE")