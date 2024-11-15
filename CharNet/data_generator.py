from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random 
import os
from matplotlib import pyplot as plt

font_folder_path = "selected_font" 

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/'] # '#' stands for '/'

def one_hot_encoder(y_value, chars):
    return np.array([1 if y_value == c else 0 for c in chars])

def one_hot_decoder(y, chars):
    return chars[list(y).index(1)]

def get_font_list(font_folder_path = "font"):
    return [f for f in os.listdir(font_folder_path) if os.path.isfile(os.path.join(font_folder_path, f))]

def generate_character_image(c, font_path, font_size = 32, image_size = (64 ,64), color_text = 255, color_background = 0):
    image_width, image_height = image_size

    img = Image.new("L", (image_width, image_height), color_background)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textlength(c, font=font) 
    text_height = font_size
    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2
    draw.text((text_x + random.randrange(-5, 5), text_y + random.randrange(-5, 5)), c, fill=color_text, font=font)

    img.filter(ImageFilter.BLUR)
    img.filter(ImageFilter.BLUR)

    img = centering(img, image_size)
    img = noise(img)

    return img

def centering(img, image_size = (64, 64)):
    crop_box = img.getbbox()
    if crop_box == None:
        return np.array(img)
    (left, top, right, bottom) = crop_box 
    img = img.crop((left, top, right, bottom))
    img = img.resize(image_size)
    return np.array(img)

import copy

def noise(img):
    noise = np.random.uniform(0, 1, size = img.shape)
    actual_noise = copy.deepcopy(noise)
    actual_noise[noise > 0.001] = 0
    actual_noise[noise <= 0.001] = random.uniform(50, 255)
    result = img + actual_noise
    result = result % 255
    return result

def generate_dataset(chars, size = 10, font_folder_path = "font"):
    X = []
    Y = []
    for char in chars:
        for font in get_font_list(font_folder_path):
            for i in range (size):
                x = generate_character_image(char, f"{font_folder_path}\\{font}")
                X.append(x)
                Y.append(one_hot_encoder(char, chars))
    X = np.array(X)
    Y = np.array(Y)
    return X, Y

if __name__ == "__main__":
    for c in chars[:4]:
        x = generate_character_image(c, font_path='./selected_font/arialbd')
        plt.imshow(x, cmap = 'gray',  vmin = 0, vmax = 255)
        plt.show()
        