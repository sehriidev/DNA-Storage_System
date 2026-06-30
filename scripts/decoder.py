from PIL import Image
import numpy as np
import os

# =========================
# LOAD DNA
# =========================

try:
    with open("dna_storage/dna_data.txt", "r") as file:
        dna_sequence = file.read().strip()

    print("[ok] DNA loaded")

except:
    print("[error] DNA file not found")
    exit()

# =========================
# LOAD METADATA
# =========================

try:
    with open("dna_storage/metadata.txt", "r") as file:
        shape_data = file.read().strip()

    h, w, c = map(int, shape_data.split(","))

    original_shape = (h, w, c)

    print("[ok] Metadata loaded")
    print("Shape:", original_shape)

except:
    print("[error] Metadata missing")
    exit()

# =========================
# DNA -> BINARY
# =========================

reverse_map = {
    "A": "00",
    "T": "01",
    "C": "10",
    "G": "11"
}

try:

    binary_string = "".join(
        reverse_map[base]
        for base in dna_sequence
    )

except:

    print("[error] Invalid DNA sequence")
    exit()

print("[ok] Binary generated")

# =========================
# BINARY -> PIXELS
# =========================

byte_list = []

for i in range(0, len(binary_string), 8):

    byte = binary_string[i:i+8]

    if len(byte) == 8:
        byte_list.append(byte)

pixels = np.array(
    [int(byte, 2) for byte in byte_list],
    dtype=np.uint8
)

print("[ok] Pixels generated")

# =========================
# VALIDATE SIZE
# =========================

required_pixels = h * w * c

if len(pixels) != required_pixels:

    print("[error] DNA and Metadata do not match")
    print("Expected:", required_pixels)
    print("Found:", len(pixels))

    exit()

# =========================
# REBUILD IMAGE
# =========================

recovered_img = pixels.reshape(original_shape)

print("[ok] Image reconstructed")

# =========================
# SAVE IMAGE
# =========================

os.makedirs("output", exist_ok=True)

import os

output_path = "output/decoded_image.png"

# Delete old image first
if os.path.exists(output_path):
    os.remove(output_path)

# Save new image
Image.fromarray(recovered_img).save(output_path)

print("[OK] New image saved")


print("[success] DECODING COMPLETE")