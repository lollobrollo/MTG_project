import numpy as np
import os
from PIL import Image
import character_classifier
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import data_generator as dg

path = "random_chars"

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '#']

def one_hot_encoder(y_value, chars):
    return np.array([1 if y_value == c else 0 for c in chars])

def one_hot_decoder(y, chars):
    return chars[list(y).index(1)]

print("Making dataset ...")
X, Y = dg.generate_dataset(chars, font_folder_path="selected_font", size = 10) # creiamo sul momento il dataset

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.2)

print("Dataset done. \n")

for i in range (10):
    img = Image.fromarray(X_train[i])
    plt.imshow(img, cmap='gray', vmin = 0, vmax = 255)
    plt.title(f'{one_hot_decoder(Y_train[i], chars)}')
    plt.show()

cnn_model = character_classifier.CharacterRecognitionCNN(num_classes=len(chars), filepath="charnet_model.keras", loading=False)
cnn_model.compile()
cnn_model.train(X_train, Y_train, X_val, Y_val, batch_size=32, epochs=10)
cnn_model.evaluate(X_test, Y_test)
cnn_model.save()
