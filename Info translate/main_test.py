import characters_detector as chs_d
import project_image
import numpy as np
from PIL import Image

real_img = Image.open("immagine_di_prova.JPG").convert("L")
img = real_img
ph = np.array(img)
im = project_image.Image2DGreyScale(ph)
im.show_image()

cd = chs_d.GSUCCharactersDetector(im)
cd.detect()
rs = cd.results()

for r in rs:
    r.show_image()


