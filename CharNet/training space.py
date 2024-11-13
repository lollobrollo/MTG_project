import PIL 
import numpy as np
import os
from PIL import Image
from matplotlib import pyplot as plt
import character_classifier
from sklearn.model_selection import train_test_split

path = "random_chars"

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/', '.']

def one_hot_encoder(y_value, chars):
    return np.array([1 if y_value == c else 0 for c in chars])

imgs_path = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
imgs_name = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

X = []
Y = []

for img_path, img_name in zip(imgs_path, imgs_name):
    img = Image.open(img_path).convert('L')
    x_img = np.array(img)
    y_img = one_hot_encoder(img_name.split('_')[1], chars)
    X.append(x_img)
    Y.append(y_img)

X = np.array(X)
Y = np.array(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15, random_state=42)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.1, random_state=42)

cnn_model = character_classifier.CharacterRecognitionCNN()
cnn_model.compile()
cnn_model.train(X_train, Y_train, X_val, Y_val)
cnn_model.evaluate(X_test, Y_test)
cnn_model.save('model_weights.h5') 





