#import characters_detector as chs_d
import project_image as pi
import numpy as np
from PIL import Image    
import character_classifier as cc
import characters_detector as cd
from matplotlib import pyplot as plt
import matplotlib.patches as patches

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/']

all_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/']

def one_hot_encoder(y_value, chars):
    return np.array([1 if y_value == c else 0 for c in chars])

def one_hot_decoder(y, chars):
    return chars[list(y).index(max(list(y)))]

def show_results(img, box_results, labels):

    plt.style.use('dark_background')

    plt.imshow(img, cmap = "gray", vmin = 0, vmax=255)
    ax = plt.gca()

    for box, lab in zip(box_results, labels):
        rect = patches.Rectangle((box[3], box[2]), box[1] - box[3], box[0] - box[2], linewidth=1, edgecolor='r', facecolor='none')
        plt.text(box[1], box[0] - 1 , lab, fontsize=8, color = 'y')
        ax.add_patch(rect)

    ax.axis('off')

    plt.show()

if __name__ == "__main__":

    bimodel = True

    im = Image.open("./foto_di_prova/5.jpeg").convert('L')
    ph = np.array(im)
    img = pi.Image2DGreyScale(ph)
    detector = cd.GSUCCharactersDetector(img)
    detector.detect()
    results = detector.resized_results(64, 64)
    results_box = detector.box_results()
    X = np.array([np.array(r.matrix) for r in results])
    
    if bimodel:
        chars_cnn = cc.CharacterRecognitionCNN(filepath="charnet_chars_model.keras", loading=True)
        chars_cnn.compile()
        chars_predictions = chars_cnn.model.predict(X)
        digits_cnn = cc.CharacterRecognitionCNN(filepath="charnet_digits_model.keras", loading=True)
        digits_cnn.compile()
        digits_predictions = digits_cnn.model.predict(X)

        show_results(im, results_box, [f"{one_hot_decoder(p[0], chars)} | {one_hot_decoder(p[1], digits)}" for p in zip(chars_predictions, digits_predictions)])

    else:
        all_chars_cnn = cc.CharacterRecognitionCNN(filepath="charnet_all_chars_model.keras", loading=True)
        all_chars_cnn.compile()
        all_chars_predictions = all_chars_cnn.model.predict(X)

        show_results(im, results_box, [f"{one_hot_decoder(p, all_chars)}" for p in all_chars_predictions])

    