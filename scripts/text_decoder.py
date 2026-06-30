# LOAD DNA
with open("dna_storage/text_dna.txt", "r") as file:
    dna_sequence = file.read()

print("[ok] DNA loaded")

# =========================
# DNA → BINARY
# =========================

reverse_map = {
    'A': '00',
    'T': '01',
    'C': '10',
    'G': '11'
}

binary_string = ''.join(
    reverse_map[base]
    for base in dna_sequence
)

print("[ok] DNA converted to binary")

# =========================
# BINARY → TEXT
# =========================

characters = []

for i in range(0, len(binary_string), 8):

    byte = binary_string[i:i+8]

    if len(byte) == 8:
        characters.append(chr(int(byte, 2)))

decoded_text = ''.join(characters)

print("[ok] Binary converted to text")

# =========================
# SAVE DECODED TEXT
# =========================

with open("output/decoded_text.txt", "w", encoding="utf-8") as file:
    file.write(decoded_text)

print("[ok] Decoded text saved")

# =========================
# SHOW RESULT
# =========================

print("\n===== RECOVERED TEXT =====\n")

print(decoded_text)

print("\n[success] TEXT DECODING COMPLETE")