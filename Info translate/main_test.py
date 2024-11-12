import characters_detector as chs_d
import image
import numpy as np

ph = np.array(([[255, 0, 255], [255, 0, 255], [255, 0, 255]]))
im = image.Image2DGreyScale(ph)
im.show_image()
cd = chs_d.GSUCCharactersDetector(im)
cd.detect()
rs = cd.results()
for r in rs:
    print(r.matrix)
    r.show_image()


