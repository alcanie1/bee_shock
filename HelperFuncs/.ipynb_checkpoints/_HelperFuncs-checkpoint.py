import numpy as np
from matplotlib import pyplot as plt
from skimage import transform as tf
import scipy.ndimage as ndi



__all__ = ['plt_channels_with_hist', 'power_is_off', 'projective_transf', 'shear', 'save_location',
          'get_bboxes', 'plot_box', 'get_mask']




def plt_channels_with_hist(img, titles=None, colors=('r','g','b'), figsize=(15,8)):
    '''
    Input: An image with a colorspace of 3 channels
    Output: None
    Subroutine: Plots all the channels along with their histograms
    '''
    if titles == None:
        titles = ('channel 1', 'channel 2', 'channel 3')
        
    channels = __get_channels(img)
    
    fig, ax = plt.subplots(ncols=2, nrows=3, figsize=figsize)
    i = 0
    for channel, title, color in zip(channels, titles, colors):
        plt.sca(ax[i][0]);
        plt.title(title)
        plt.imshow(channel)
        plt.sca(ax[i][1])
        plt.title(f'{title} hist')
        plt.hist(np.ravel(channel), color=color)
        i += 1

    
def __get_channels(img):
    channel_1 = img[...,0]
    channel_2 = img[...,1]
    channel_3 = img[...,2]
    return (channel_1, channel_2, channel_3)


def power_is_off(img):
    '''
    Input: An RGB image of shock bee experiment
    Output: Boolean indicating if shock is off
    '''
    threshold = 50_000
    red_chan = img[...,0]
    freq, _ = np.histogram(np.ravel(red_chan))
    
    if freq[0] >= threshold:
        return True
    
    else:
        return False


def shear(image, shear, **kwargs):
    
    if 'order' not in kwargs:
        kwargs['order'] = 0
    
    transform = tf.AffineTransform(shear=shear)
    return tf.warp(image, transform, preserve_range=True,
                    **kwargs).astype('uint8') 



def projective_transf(img, src=[], dst=[], **kwargs):
    
    if src==[] or dst==[]:
        raise("Missing argument: src and dst keyword arguments are required.")
        
    tform = tf.estimate_transform('projective', src, dst)
    transformed_img = tf.warp(img, inverse_map=tform.inverse, **kwargs)
    
    return transformed_img



def save_location(coords, bee_locations):
    # CELLS[0] is the Cell 1 in the image (The one without a bee) and its pair values are (x1, x2) 
    CELLS = [(0, 51), (51, 110),(110, 160), (160, 210), (210, 270), (270, 320), (320, 380), (380, 430), (430,490), (490, 540)]
    HEIGHT = 150
    
    m = 0
    for x,y in coords:
        for i,j in CELLS:
            
            if i < x and x < j:

                if y > HEIGHT:
                    # Is in yellow area
                    bee_locations[m].append(1)

                else:
                    # Is in blue area
                    bee_locations[m].append(0)
                

            m = m + 1
        m = 0   
        
        
def plot_box(box, **kargs):
    # box: in (min_row, min_col, max_row, max_col) format (make sure you use correct order)
    [y1,x1,y2,x2] = box
    plt.plot([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1],**kargs)

    
def get_bboxes(label_bees):
    bboxes = [] # Coords
            for region in measure.regionprops(label_bees):
                if region.area >= 100:
                    min_row, min_col, max_row, max_col = region.bbox
                    bboxes.append([min_row, min_col, max_row, max_col])
    
    return bboxes

def get_mask(img):
    # Values for projective transform
    src = np.array([[70, 25], [600, 9], [609, 312], [40, 310]])
    dst = np.array([[65, 10], [600, 10], [600, 315], [65, 315]])
    
    img_projected = projective_transf(img, src=src, dst=dst, output_shape=(325, 640))
    hsv_img_projected = color.rgb2hsv(img_projected)
    hsv_img_projected = hsv_img_projected[0:310 , 60:600, :]
    mask = (hsv_img_projected[...,0] <= 0.25) & (hsv_img_projected[...,2] <= 0.4)
    mask = ndi.median_filter(mask, size=5)
    return mask


def label_image_regions(img ):
    label_image = morph.label(morphed)
    image_label_overlay = color.label2rgb(label_image, image=hsv_img_projected)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(image_label_overlay)

    Coords = []

    for region in regionprops(label_image):
        if region.area >= 50:


            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)

            x = (maxc + minc)/ 2
            y = (maxr + minr)/ 2

            Coords.append((x, y))

            #Good for single image slices
            #bee = (0 < mask).astype(int)
            #properties = measure.regionprops(bee, mask) #region props ignores all 0's
            #center_of_mass = properties[0].centroid

            #print(center_of_mass)

            #y,x = center_of_mass 

