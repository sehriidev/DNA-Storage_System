import random

# LOAD ORIGINAL DNA
with open("dna_storage/dna_data.txt", "r") as file:
    dna_sequence = file.read()

print("[ok] Original DNA loaded")

# DNA bases
bases = ['A', 'T', 'C', 'G']

# convert string → list
dna_list = list(dna_sequence)

# introduce random errors
num_errors = 100

for _ in range(num_errors):

    index = random.randint(0, len(dna_list) - 1)

    original_base = dna_list[index]

    possible_bases = [b for b in bases if b != original_base]

    dna_list[index] = random.choice(possible_bases)

# corrupted DNA
corrupted_dna = ''.join(dna_list)

print("[ok] DNA corruption complete")

# SAVE CORRUPTED DNA
with open("dna_storage/corrupted_dna.txt", "w") as file:
    file.write(corrupted_dna)

print("[ok] Corrupted DNA saved")

print("\n[sucess] ERROR SIMULATION COMPLETE")