#import characters_detector as chs_d
import project_image
import numpy as np
from PIL import Image    
import character_classifier as cc

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/', '.']

def one_hot_encoder(y_value, chars):
    return np.array([1 if y_value == c else 0 for c in chars])

def one_hot_encoder_m(y_value, chars, m):
    return np.array([one_hot_encoder(y_value, chars) for n in range (m)])

x = np.array([np.random.random((64, 64)) for i in range (5)])
y = one_hot_encoder_m('A', chars, 5)

x_val = np.array([np.random.random((64, 64)) for i in range (5)])
y_val = one_hot_encoder_m('A', chars, 5)

cnn = cc.CharacterRecognitionCNN(num_classes=len(chars))
cnn.compile()
cnn.train(x, y, x_val, y_val)