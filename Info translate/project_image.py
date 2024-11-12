import numpy as np
import copy
from matplotlib import pyplot as plt
from PIL import Image

"""
We define our img class. We store our images as numpy ndarray but for utility we implement here a class 
with util functions.
"""

class Image2DGreyScale:
    def __init__(self, matrix):
        """
        We do initialize our img just py copying a np.ndarray containig everything we need. 
        We assume that our matrix has only 1 channel of color (grey scale).
        The matrix then has to contain only integers.

        Parameters:
        matrix (matrix) : the matrix to copy. it should be a numpy ndarray of shape (x, y, 1) and of dtype=int.        
        """
        if not type(matrix) == np.ndarray:
            raise TypeError(f"An Exception occours while initializing a Image2D object. You should pass an np.ndarray as input.\nFound {type(matrix)}")
        if not matrix.ndim == 2:
            raise TypeError(f"An Exception occours while initializing a Image2D object. You should pass an np.ndarray with ndim == 2.\nFound {matrix.ndim}.")
        height, width = matrix.shape 
        self.matrix = copy.deepcopy(matrix)
        self.height = height
        self.width = width

    def show_image(self):
        plt.imshow(self.matrix, cmap='gray',  vmin=0, vmax=256) 
        plt.show()

    def get_portion_of_image(self, min_y, min_x, max_y, max_x):
        """
        This function return a portion of the image using the coordinates given to compute a rectangle.

        Parameters:
        min_y (int) : bottom margin index.
        min_x (int) : right margin index.
        max_y (int) : top margin index.
        max_x (int) : left margin index.

        Returns:
        A new image representing the portion of image desired.
        """
        portion = copy.deepcopy(self.matrix[min_y:max_y, min_x: max_x])
        return Image2DGreyScale(portion)
    
    def __str__(self):
        return str(self.matrix)

    def resize(self, new_width = 100, new_height = 150):
        p = Image.fromarray(self.matrix)
        p = p.resize([new_width, new_height])
        p = np.array(p)
        self.matrix = copy.deepcopy(p)
        self.width = new_width
        self.height = new_height

