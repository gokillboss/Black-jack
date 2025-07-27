from PIL import Image, ImageDraw
import os

CARD_DIR = "assets/card_images"
PADDING = 8         # khoảng trắng xung quanh
RADIUS = 15         # bo góc
BG_COLOR = (45, 90, 61, 255)   # nền trắng

def add_rounded_corners(im, radius):
    """Tạo mask bo góc cho ảnh."""
    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, im.size[0], im.size[1]], radius=radius, fill=255)
    im.putalpha(mask)
    return im

for filename in os.listdir(CARD_DIR):
    if filename.endswith(".png"):
        path = os.path.join(CARD_DIR, filename)
        img = Image.open(path).convert("RGBA")

        # Bo góc ảnh gốc
        img = add_rounded_corners(img, RADIUS)

        # Tạo canvas với padding và nền trắng
        new_size = (img.width + PADDING * 2, img.height + PADDING * 2)
        canvas = Image.new("RGBA", new_size, BG_COLOR)
        canvas.paste(img, (PADDING, PADDING), img)

        # Lưu lại
        canvas.save(path, "PNG")
        print(f"Đã xử lý {filename}")

print("✅ Hoàn tất bo góc + padding + nền trắng!")
