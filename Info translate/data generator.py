from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random 

font_path = "./comfortaa/Comfortaa-Regular.ttf" 

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

    img.save(f"./data for training/{name}.png")

def random_modify(img):
    k = random.randint(0, 360)
    rotated_img = img.rotate(k, expand=False)
    resized_img = rotated_img.resize(img.size)
    f = random.randint(0, 1)
    if f == 0:
        result = resized_img.filter(ImageFilter.BLUR)
    if f == 1:
        result = resized_img.filter(ImageFilter.DETAIL)
    return result


def generate_dataset(chars, size):
    for char in chars:
        for i in range (size):
            if char == '/':
                generate_character_image(char, f"#_{i}", font_path) # this is special
            generate_character_image(char, f"{char}_{i}", font_path)

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/', '.']

generate_dataset(chars, 100)