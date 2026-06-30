import sys
from PIL import Image
import numpy as np
import sys

image_path = sys.argv[1]

print("Selected Image =", image_path)


img = Image.open(image_path)

print("Image mode:", img.mode)

# convert to RGB
img = img.convert("RGB")

# convert image to numpy array
img_array = np.array(img)

print("First 20 pixel values:")
print(img_array.flatten()[:20])

# save original shape
original_shape = img_array.shape

print("[ok] Image loaded")
print("Shape:", original_shape)

# =========================
# IMAGE → BINARY
# =========================

flat_pixels = img_array.flatten()

binary_data = [format(pixel, '08b') for pixel in flat_pixels]

print("[ok] Binary conversion complete")

# =========================
# BINARY → DNA
# =========================

dna_map = {
    "00": "A",
    "01": "T",
    "10": "C",
    "11": "G"
}

all_bits = ''.join(binary_data)

dna_sequence = ''.join(
    dna_map[all_bits[i:i+2]]
    for i in range(0, len(all_bits), 2)
)

print("[ok] DNA encoding complete")

# =========================
# SAVE DNA
# =========================

with open("dna_storage/dna_data.txt", "w") as file:
    file.write(dna_sequence)

print("[ok] DNA saved")

# =========================
# SAVE METADATA
# =========================

with open("dna_storage/metadata.txt", "w") as file:
    file.write(
        f"{original_shape[0]},"
        f"{original_shape[1]},"
        f"{original_shape[2]}"
    )
print("First 64 bits:")
print(all_bits[:64])

print("First 50 DNA bases:")
print(dna_sequence[:50])
print("[ok] Metadata saved")

print("\n[success] ENCODING COMPLETE")
# Remove old decoded image so Streamlit cannot show cached image
import os

if os.path.exists("output/decoded_image.png"):
    os.remove("output/decoded_image.png")