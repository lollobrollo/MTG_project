import keras
import numpy

"""
This model will be a CNN. 
"""

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

class CharacterRecognitionCNN:
    def __init__(self, input_shape=(64, 64, 1), num_classes=128):
        self.model = Sequential([
            Conv2D(16, kernel_size=(3, 3), activation='relu', input_shape=input_shape),
            MaxPooling2D(pool_size=(2, 2)),

            Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape),
            MaxPooling2D(pool_size=(2, 2)),

            Conv2D(64, kernel_size=(3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
    
            Conv2D(128, kernel_size=(3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
  
            Dense(num_classes, activation='softmax')
        ])

    def compile(self, learning_rate=0.001):
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])
    
    def summary(self):
        self.model.summary()
        
    def train(self, x_train, y_train, x_val, y_val, epochs=10, batch_size=32):
        history = self.model.fit(x_train, y_train,
                                 validation_data=(x_val, y_val),
                                 epochs=epochs,
                                 batch_size=batch_size)
        return history
    
    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test)

cnn = CharacterRecognitionCNN(input_shape=(64, 64, 1), num_classes=62)
cnn.compile(learning_rate=0.001)
cnn.summary()

