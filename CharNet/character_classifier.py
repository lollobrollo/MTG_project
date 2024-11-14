import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

"""
This model will be a CNN. 
"""

class CharacterRecognitionCNN:
    def __init__(self, filepath, loading = False, input_shape=(64, 64, 1), num_classes=38):
        self.filepath = filepath
        if not loading:
            self.model = Sequential([
                Conv2D(32, kernel_size=(3, 3), activation='relu', padding = 'same', input_shape=input_shape),
                MaxPooling2D(pool_size=(2, 2)),

                Conv2D(64, kernel_size=(3, 3), activation='relu', padding = 'same'),
                MaxPooling2D(pool_size=(2, 2)),
        
                Conv2D(128, kernel_size=(3, 3), activation='relu', padding = 'same'),
                MaxPooling2D(pool_size=(2, 2)),
                
                Flatten(),
                Dense(128, activation='relu'),

                Dense(62, activation='relu'),
    
                Dense(num_classes, activation='softmax')
            ])
        else:
            self.load()

    def compile(self, learning_rate=0.001):
        self.model.compile(optimizer=keras.optimizers.RMSprop(learning_rate),
                           loss='categorical_crossentropy',
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
    
    def save(self):
        keras.saving.save_model(self.model, self.filepath)

    def load(self):
        self.model = keras.saving.load_model(self.filepath)
        
    def __call__(self, *args, **kwds):
        self.model.__call__(*args, **kwds)


