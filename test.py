from PIL import Image

SRC = "assets/pac_man_title/pac _man _ tile _ 1.png"
DST = "assets/pac_man_title/pac_man_title_transparent.png"

img = Image.open(SRC).convert("RGBA")
pixels = img.load()
width, height = img.size

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        # Near-white and light-gray pixels with no color = checkerboard squares
        if min(r, g, b) >= 200 and max(r, g, b) - min(r, g, b) <= 12:
            pixels[x, y] = (r, g, b, 0)

img.save(DST)