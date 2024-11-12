"""
We just have an incredible idea to implement the single-character detector: 
we will use a nice unsupervised learning algorithm :)
how? well... we will use an activation function on the image, so that our 
pixels will be or 0 or 1. then we will connect every single 1 to every other 1
that can be directly connected. Since our character (thanks to the font
used by MTG) are all fully connected (that means, for example i is not written
with the cap point bus is written as I), we know for sure that our characters are
all separated by the others. So we can build 'cluster' of this and every cluster
will just be a single character. we can build a rectangle using the min_X, max_X, 
min_Y, max_y along all the points in the clusters and the job is done.
We can even "chain" the characters into words looking at the distances between 
centroid of the clusters.
Pretty clever, isn't it?
"""
        
import image
import copy
import networkx as nx

class CharactersDetector():

    def __init__(self, img):
        """
        Initialize a CharactersDetector. 
        The particular type of CharactersDetectors depends on the task.
         
        Parameters:
        img (img type) : The image containing the text where to detect the characters.
        """
        self.img = copy.deepcopy(img)

    def detect(self):
        """
        This is method that returns the characters separated in differents images.

        Returns:
        list of img type: The images containing the raw characters. 
        """
        return None
        
class GSUCCharactersDetector(CharactersDetector):
    def __init__(self, img, threshold = 122):
        """
        This is the class suited for detecting upper case text in a Image2DGreyScale object.

        Parameters:
        img (must be a GreyScaleImage2D object) : the image containing the text.
        threshold (int) : the threshold used for the aactivation. Default is 122.
        """
        if not type(img) == image.Image2DGreyScale:
            raise TypeError(f"An Exception occours while initializing a GSUCCharactersDetector object. The image type must be Image2DGreyScale.\nFound{type(img)}")
        super().__init__(img)
        if threshold > 225 or threshold < 0:
            raise ValueError(f"An Exception occours while initializing a GSUCCharactersDetector object. The threshold value must be in the range 0, 255.")
        self.__threshold = threshold
        self.__result = []
        self.__detected = False
    
    def detect(self):
        self.__activate()
        graph = {}
        for i in range (0, self.img.height):
            for j in range (0, self.img.width):
                if self.img.matrix[i, j] == 255:
                    t = []
                    for idx in self.__neighbors(i, j):
                        if self.img.matrix[idx] == 255:
                            t.append(idx)
                    graph[(i, j)] = copy.deepcopy(t)
        G = nx.from_dict_of_lists(graph)
        S = list(nx.connected_components(G))
        print(S)
        for char in S:
            min_y, min_x, max_y, max_x = self.img.height, self.img.width, 0, 0
            for x, y in char:
                min_y, min_x, max_y, max_x = min(min_y, y), min(min_x, x), max(max_y, y), max(max_x, x)
            max_x, max_y = (max_x + (max_x == min_x)), (max_y + (max_y == min_y))
            print(f'{min_x} : {max_x} ; {min_y} : {max_y}')
            self.__result.append(self.img.get_portion_of_image(min_y, min_x, max_y, max_x))          
        self.__detected = True 

    def __activate(self):
        """
        This function just set to 255 every bit greater than the thresholds and to 0 every bit smaller than it.
        """
        self.img.matrix[self.img.matrix > self.__threshold] = 255
        self.img.matrix[self.img.matrix <= self.__threshold] = 0

    def results(self):
        if self.__detected == False:
            raise Exception("Results not computed yet. Compute them with the detect method.")
        return self.__result

    def __neighbors(self, i, j):
        neigh = []
        for z in range (i-1, i+2):
            for w in range (j-1, j+2):
                if z != i and w == j:
                    if z >= 0 and z < self.img.height:
                        neigh.append((z, j))
                if z == i and w != j:
                    if w >= 0 and w < self.img.width:
                        neigh.append((i, w))
        return neigh