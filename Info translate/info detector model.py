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
        
class SingleCharactersDetector():
    pass
