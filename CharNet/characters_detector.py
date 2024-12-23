import project_image
import copy
import networkx as nx
import matplotlib.pyplot as plt

class CharactersDetector():

    def __init__(self, img):
        """
        Initialize a CharactersDetector. 
        The particular type of CharactersDetectors depends on the task.
        
        Parameters:
        img (img type) : The image containing the text where to detect the characters.
        """
        self.img = copy.deepcopy(img)
        self.working_img = copy.deepcopy(img) # this is the actually img that we activate and work on

    def detect(self):
        """
        This is method that returns the characters separated in differents images.

        Returns:
        list of img type: The images containing the raw characters. 
        """
        return None
        
class GSUCCharactersDetector(CharactersDetector):
    def __init__(self, img, threshold = 50):
        """
        This is the class suited for detecting upper case text in a Image2DGreyScale object.

        Parameters:
        img (must be a GreyScaleImage2D object) : the image containing the text.
        threshold (int) : the threshold used for the aactivation. Default is 50.
        """
        if not type(img) == project_image.Image2DGreyScale:
            raise TypeError(f"An Exception occours while initializing a GSUCCharactersDetector object. The image type must be Image2DGreyScale.\nFound{type(img)}")
        super().__init__(img)
        if threshold > 225 or threshold < 0:
            raise ValueError(f"An Exception occours while initializing a GSUCCharactersDetector object. The threshold value must be in the range 0, 255.")
        self.__threshold = threshold
        self.__result = []
        self.__box_result = []
        self.__centers = []
        self.__avg_height = 0
        self.__detected = False
        self.__indexes = {}
    
    def detect(self):
        """
        This is the core method of the class. Call this to detect the differents characters separately. 
        The actual idea of this method is that we set every pixel either to 0 or to 255.
        Then we create the graph of the image, connecting with a crossneighbor all the 255 near. 
        On the graoh we compute the connected compnonents and ta-dà: our characters are recognized.
        """
        if self.__detected == False:
            self.__activate()
            G = self.__graph_of_chars() # This is the graph representation of the img
            S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
            tot_h = 0
            for char in S:
                min_y, min_x, max_y, max_x = self.img.height, self.img.width, 0, 0
                for y, x in char:
                    min_y, min_x, max_y, max_x = min(min_y, y), min(min_x, x), max(max_y, y), max(max_x, x)
                self.__result.append(self.img.get_portion_of_image(min_y, min_x, max_y + 1, max_x + 1))
                self.__box_result.append((min_y, min_x, max_y + 1, max_x + 1))          
                self.__centers.append(((max_y - min_y)/2,(max_x - min_x)/2))
                tot_h += (max_y - min_y)
            self.__avg_height = tot_h / len(S)
            self.__detected = True 

        else:
            print("Detection already done. Access the results via obectj_name.result")

    def __activate(self):
        """
        This function just set to 255 every bit greater than the thresholds and to 0 every bit smaller than it.
        """
        self.working_img.matrix[self.img.matrix > self.__threshold] = 255
        self.working_img.matrix[self.img.matrix <= self.__threshold] = 0

    def results(self):
        if self.__detected == False:
            self.detect()
        return self.__result
    
    def box_results(self):
        if self.__detected == False:
            self.detect()
        return self.__box_result

    def centers(self):
        if self.__detected == False:
            self.detect()
        return self.__centers
    
    def indexes(self):
        pass
        

    def resized_results(self, new_width, new_height):
        for i in range (len(self.__result)):
            self.__result[i].resize(new_width, new_height)
        return self.__result
    
    def __graph_of_chars(self):
        graph = {}
        for i in range (0, self.img.height):
            for j in range (0, self.img.width):
                if self.working_img.matrix[i, j] == 255:
                    t = []
                    for idx in self.__neighbors(i, j):
                        if self.working_img.matrix[idx] == 255:
                            t.append(idx)
                    graph[(i, j)] = copy.deepcopy(t)
        G = nx.from_dict_of_lists(graph)
        return G

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
    
if __name__ == "__main__":
    pass