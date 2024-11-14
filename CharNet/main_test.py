#import characters_detector as chs_d
import project_image as pi
import numpy as np
from PIL import Image    
import character_classifier as cc
import characters_detector as cd

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/']

def one_hot_encoder(y_value, chars):
    return np.array([1 if y_value == c else 0 for c in chars])

def one_hot_decoder(y, chars):
    return chars[list(y).index(max(list(y)))]

if __name__ == "__main__":
    im = Image.open("immagine_di_prova.JPG").convert('L')
    ph = np.array(im)
    img = pi.Image2DGreyScale(ph)
    detector = cd.GSUCCharactersDetector(img)
    detector.detect()
    results = detector.resized_results(64, 64)
    X = np.array([np.array(r.matrix) for r in results])
    chars_cnn = cc.CharacterRecognitionCNN(filepath="charnet_chars_model.keras", loading=True)
    chars_cnn.compile()
    chars_predictions = chars_cnn.model.predict(X)
    digits_cnn = cc.CharacterRecognitionCNN(filepath="charnet_digits_model.keras", loading=True)
    digits_cnn.compile()
    digits_predictions = digits_cnn.model.predict(X)

    for r, p in zip(results, zip(chars_predictions, digits_predictions)):
        r.show_image(label = f"CHAR_CNN : {one_hot_decoder(p[0], chars)} / DIGITS_CNN = {one_hot_decoder(p[1], digits)}")