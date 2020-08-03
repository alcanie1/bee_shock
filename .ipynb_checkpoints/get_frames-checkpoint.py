import av
from skimage import io, measure, color
import HelperFuncs as hf
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import scipy.ndimage as ndi


VIDEO_PATH = './Data/video_footage.mp4'
IMG_STORAGE_PATH = './Data/'
IMG_SEG_STORAGE_PATH = './Data3/'


def _plot_frames():
    '''
    Use this function if you just want to plot every frame
    '''
    
    video = av.open(VIDEO_PATH)
    
    on_count = off_count = 1
    for i, frame in enumerate(video.decode(video=0)):
        img = frame.to_image().convert('RGB')
        img = np.array(img)

        if hf.power_is_off(img):
            plt.imshow(img)
            plt.title(f'OFF# {off_count}')
            off_count += 1

        else:
            plt.imshow(img)
            plt.title(f'ON# {on_count}')
            on_count += 1

        plt.show()

        
def _video_to_imgs():
    '''
    Use this function to save every frame of the video as an image at path IMG_STORAGE_PATH
    '''
    
    video = av.open(VIDEO_PATH)
    
    on_count = off_count = 1
    for i, frame in enumerate(video.decode(video=0)):
        img = frame.to_image().convert('RGB')
        img = np.array(img)
    
        if i == 398:
            outpath = f'frame_{i}.jpg'
            io.imsave(outpath, img)
            break
            
        # if hf.power_is_off(img):
        #     outpath = f'{IMG_STORAGE_PATH}OFF_{off_count}.jpg'
        #     io.imsave(outpath, img)
        #     off_count += 1

        # else:
        #     outpath = f'{IMG_STORAGE_PATH}ON_{on_count}.jpg'
        #     io.imsave(outpath, img)
        #     on_count += 1

            
def _count_frames():
    
    video = av.open(VIDEO_PATH)
    
    counter = 0
    for i, frame in enumerate(video.decode(video=0)):
        counter += 1
            
    print(counter)
    
def count_zeros_and_ones(arr):
    zero_counter = 0
    ones_counter = 0
    for i in arr:
        if i == 1:
            ones_counter += 1
            
        elif i == 0:
            zero_counter += 1
        
    return (ones_counter, zero_counter)
    
    
def segment_bees():

    print('Processing ... ')
    
    # bee_locations[bee_number][locations (0 for blue & 1 for yellow)]
    bee_locations = [ [], [], [], [], [], [], [], [], [], [] ]

    # Values for projective transform
    src = np.array([[70, 25], [600, 9], [609, 312], [40, 310]])
    dst = np.array([[65, 10], [600, 10], [600, 315], [65, 315]])

    video = av.open(VIDEO_PATH)
    frames_with_pw_off = 0
    for i, frame in enumerate(video.decode(video=0)):
        img = frame.to_image().convert('RGB')
        img = np.array(img)

        if not hf.power_is_off(img):
            img_projected = hf.projective_transf(img, src=src, dst=dst, output_shape=(325, 640))
            hsv_img_projected = color.rgb2hsv(img_projected)
            hsv_img_projected = hsv_img_projected[0:310 , 60:600, :]
            mask = (hsv_img_projected[...,0] <= 0.25) & (hsv_img_projected[...,2] <= 0.4)
            mask = ndi.median_filter(mask, size=9)
            label_bees = measure.label(mask)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(color.hsv2rgb(hsv_img_projected))
            
            coords = []
            for region in measure.regionprops(label_bees):
                if region.area >= 110:


                    minr, minc, maxr, maxc = region.bbox
                    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=2)
                    ax.add_patch(rect)

                    x = (maxc + minc)/ 2
                    y = (maxr + minr)/ 2

                    coords.append((x, y))
                    
            hf.save_location(coords, bee_locations)
            plt.axis('off')
            plt.savefig(f'{IMG_SEG_STORAGE_PATH}frame_{i}.jpg', bbox_inches='tight', pad_inches=0)
            plt.close(plt.gcf())
        
        else:
            frames_with_pw_off += 1
            img_projected = hf.projective_transf(img, src=src, dst=dst, output_shape=(325, 640))
            img_projected = img_projected[0:310 , 60:600, :]
            plt.figure(figsize=(10, 6))
            plt.imshow(img_projected)
            plt.axis('off')
            plt.savefig(f'{IMG_SEG_STORAGE_PATH}frame_{i}.jpg', bbox_inches='tight', pad_inches=0)
            plt.close(plt.gcf())
            
        
    print('Done')

    return (bee_locations, frames_with_pw_off)


def main():
    
    bee_locations, count_pw_off_frames = segment_bees()

    print('Running statistics ... ')
    bee_locations = np.array(bee_locations)
    
    total_ones = []
    total_zeros = []
    
    for i, arr in enumerate(bee_locations):
        ones, zeros = count_zeros_and_ones(arr)
        total_ones[i] = ones
        total_zeros[i] = zeros
    
    print(f'Frames with power off: {frames_with_pw_off}')
    
    for i in range(total_ones):
        print(f'Bee_{i} in yellow: {total_ones[i]} \t in blue: {total_zeros[i]}')

    # _video_to_imgs()
    
    


if __name__ == '__main__':
    main()
