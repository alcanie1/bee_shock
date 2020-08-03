import numpy as np
from matplotlib import pyplot as plt
from skimage import io

IMG_PATH = './Data/'
XY_TICK_STEPS = 25

img = io.imread(f'{IMG_PATH}ON_0.jpeg')

plt.imshow(img)
plt.grid(True)
plt.xticks(np.arange(0,640,XY_TICK_STEPS))
plt.yticks(np.arange(0,480,XY_TICK_STEPS));
plt.show()