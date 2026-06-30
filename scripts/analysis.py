# LOAD ORIGINAL DNA
with open("dna_storage/dna_data.txt", "r") as file:
    original_dna = file.read()

# LOAD CORRUPTED DNA
with open("dna_storage/corrupted_dna.txt", "r") as file:
    corrupted_dna = file.read()

print("[ok] DNA files loaded")

# =========================
# COUNT ERRORS
# =========================

errors = 0

for a, b in zip(original_dna, corrupted_dna):
    if a != b:
        errors += 1

# total bases
total_bases = len(original_dna)

# accuracy
accuracy = ((total_bases - errors) / total_bases) * 100

# =========================
# RESULTS
# =========================

print("\n===== DNA STORAGE ANALYSIS =====")

print("Total DNA bases:", total_bases)

print("Total corrupted bases:", errors)

print("Storage accuracy:", round(accuracy, 5), "%")

print("\n[success] ANALYSIS COMPLETE")