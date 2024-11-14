import numpy as np
import os
from PIL import Image
import character_classifier
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import data_generator as dg

def one_hot_encoder(y_value, chars):
    return np.array([1 if y_value == c else 0 for c in chars])

def one_hot_decoder(y, chars):
    return chars[list(y).index(1)]

if __name__ == "__main__":

    # CHARS MODEL
    
    chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    chars_model = character_classifier.CharacterRecognitionCNN(num_classes=len(chars), filepath="charnet_chars_model.keras", loading=False)

    print("Making dataset for chars ...")

    X, Y = dg.generate_dataset(chars, font_folder_path="font", size = 10) # creiamo sul momento il dataset

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.2)

    print("Dataset done. \n")

    chars_model.compile()
    chars_model.train(X_train, Y_train, X_val, Y_val, batch_size=64, epochs=10)
    chars_model.evaluate(X_test, Y_test)
    chars_model.save()

    # DIGITS MODEL

    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/']

    digits_model = character_classifier.CharacterRecognitionCNN(num_classes=len(digits), filepath="charnet_digits_model.keras", loading=False)

    print("Making dataset for digits ...")

    X, Y = dg.generate_dataset(digits, font_folder_path="font", size = 10) # creiamo sul momento il dataset

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.2)

    print("Dataset done. \n")

    digits_model.compile()
    digits_model.train(X_train, Y_train, X_val, Y_val, batch_size=32, epochs=5)
    digits_model.evaluate(X_test, Y_test)
    digits_model.save()
