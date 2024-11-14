from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random 
import os

font_folder_path = "font" 

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '#'] # '#' stands for '/'

def one_hot_encoder(y_value, chars):
    return np.array([1 if y_value == c else 0 for c in chars])

def one_hot_decoder(y, chars):
    return chars[list(y).index(1)]

def get_font_list(font_folder_path = "font"):
    return [f for f in os.listdir(font_folder_path) if os.path.isfile(os.path.join(font_folder_path, f))]

def generate_character_image(c, font_path, font_size = 48, image_size = (64 ,64), color_text = 255, color_background = 0):
    image_width, image_height = image_size

    img = Image.new("L", (image_width, image_height), color_background)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textlength(c if c != '#' else '/', font=font) # We use '#' as placeholder for the '/' (cuz we have problem in saving '/' as name)
    text_height = font_size
    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2
    draw.text((text_x, text_y), c, fill=color_text, font=font)

    img = random_noise(img)
    return img

def random_noise(img):
    img = np.array(img)
    noise = np.random.uniform(0, 1, img.shape)
    actual_noise = np.array([[random.randint(100, 255) if n < 0.03 else 0 for n in nn] for nn in noise])
    result = (actual_noise + img).astype(np.uint8)
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
