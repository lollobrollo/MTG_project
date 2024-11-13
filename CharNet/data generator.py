from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random 
import os

font_folder_path = "font" 

def get_font_list(font_folder_path):
    return [f for f in os.listdir(font_folder_path) if os.path.isfile(os.path.join(font_folder_path, f))]

def generate_character_image(c, name, font_path, font_size = 64, image_size = (64 ,64), color_text = 255, color_background = 0):
    image_width, image_height = image_size

    img = Image.new("L", (image_width, image_height), color_background)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textlength(c, font=font)
    text_height = font_size
    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2
    draw.text((text_x, text_y), c, fill=color_text, font=font)

    img = random_modify(img)

    img.save(f"./random_chars/{name}.png")

def random_modify(img):
    # we do not include rotation
    f = random.randint(0, 1)
    if f == 0:
        result = img.filter(ImageFilter.BLUR)
    if f == 1:
        result = img.filter(ImageFilter.DETAIL)
    img = np.array(img)
    noise = np.random.uniform(0, 1, img.shape)
    actual_noise = np.array([[random.randint(100, 255) if n < 0.03 else 0 for n in nn] for nn in noise])
    result = actual_noise + result
    return Image.fromarray(result).convert('L')


def generate_dataset(chars, font_folder_path, size):
    for char in chars:
        for j, font in enumerate(get_font_list(font_folder_path)):
            for i in range (size):
                generate_character_image(char, f"{char}_{i}_{j}", f"{font_folder_path}/{font}")

#chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
#             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/', '.']
chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
generate_dataset(chars, font_folder_path, 10)

