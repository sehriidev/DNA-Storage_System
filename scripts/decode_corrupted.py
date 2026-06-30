from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# =========================
# LOAD CORRUPTED DNA
# =========================

with open("dna_storage/corrupted_dna.txt", "r") as file:
    dna_sequence = file.read()

print("✅ Corrupted DNA loaded")

# =========================
# LOAD METADATA
# =========================

with open("dna_storage/metadata.txt", "r") as file:
    shape_data = file.read()

h, w, c = map(int, shape_data.split(','))

original_shape = (h, w, c)

print("✅ Metadata loaded")

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

print("✅ DNA decoded to binary")

# =========================
# BINARY → PIXELS
# =========================

byte_list = [
    binary_string[i:i+8]
    for i in range(0, len(binary_string), 8)
]

pixels = np.array(
    [int(byte, 2) for byte in byte_list],
    dtype=np.uint8
)

print("✅ Binary converted to pixels")

# =========================
# REBUILD IMAGE
# =========================

recovered_img = pixels.reshape(original_shape)

print("✅ Corrupted image reconstructed")

# =========================
# SHOW IMAGE
# =========================

plt.imshow(recovered_img)
plt.title("Image Decoded From Corrupted DNA")
plt.axis('off')
plt.show()

# =========================
# SAVE IMAGE
# =========================

final_image = Image.fromarray(recovered_img)

final_image.save("output/corrupted_decoded_image.png")

print("✅ Corrupted decoded image saved")

print("\n🎉 CORRUPTED DNA DECODING COMPLETE")