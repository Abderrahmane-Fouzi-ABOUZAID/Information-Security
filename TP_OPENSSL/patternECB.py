from PIL import Image

with open("classified.enc", "rb") as f:
    content = f.read()

header_size = 16
ciphertext = content[header_size:]

width, height = 432, 475
expected_size = width * height
ciphertext = ciphertext[:expected_size]

block_size = 16
blocks = [ciphertext[i : i + block_size] for i in range(0, len(ciphertext), block_size)]

unique_blocks = sorted(list(set(blocks)))
num_unique = len(unique_blocks)

block_to_gray = {}
for idx, block in enumerate(unique_blocks):
    gray_val = int((idx * 255) / max(1, num_unique - 1))
    block_to_gray[block] = gray_val

new_pixels = bytearray()
for block in blocks:
    gray_val = block_to_gray[block]
    new_pixels.extend(bytes([gray_val] * block_size))

img = Image.frombytes("L", (width, height), bytes(new_pixels))
img.save("pattern_ecb.png")
print("Successfully generated and saved pattern_ecb.png!")
