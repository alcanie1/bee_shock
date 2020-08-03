import numpy as np
from skimage import transform as tf
from enum import Enum, unique


@unique
class Color(Enum):
    Red = 0
    Green = 1
    Blue = 2


class ImgManipulator(object):


    def projective_transform(self, img, src=None, dst=None, **kwargs):
        """
        Applies projective transform to a given image.

        This method requires the skimage module. Visit the following link
        https://scikit-image.org/docs/dev/install.html for information on
        how to install it. 
        Note: If the optional arguments src and dst are not provided it will use
        values that work specifically for the bee shock project.

        Typical usage example:

        img_manipulator = ImgManipulator()
        
        a_white_image = np.ones((700, 700, 3), dtype=np.uint8) * 255
        source = np.array([[70, 25], [600, 9], [609, 312], [40, 310]])
        destination = np.array([[65, 10], [600, 10], [600, 315], [65, 315]])

        result_img = img_manipulator.projective_transform(
            a_white_image, src=source, 
            dst=destination, output_shape=(325, 640))

        Args:
            img: An image as numpy array.
            src (list<list>): A list of integers of the desired source coordinates in the image.
            dst (list<list>): A list of integers of the desired destination coordinates in the image.
            **kwargs: Optional keyword arguments given to skimage.transform.warp 

        Returns:
            An image with projective transform applied to it.
        """

        if src is None or dst is None:
            src = np.array([[70, 25], [600, 9], [609, 312], [40, 310]])
            dst = np.array([[65, 10], [600, 10], [600, 315], [65, 315]])

        tform = tf.estimate_transform('projective', src, dst)
    
        return tf.warp(img, inverse_map=tform.inverse, **kwargs)


    def crop(self, img, x_range, y_range):
        x_start, x_finish = x_range
        y_start, y_finish = y_range

        return img[y_start : y_finish, x_start : x_finish, :]


    def add_bounding_boxes(self, img, bboxes, color=None):
        """
        Note: img must be of type np.uint8
        bboxes order: [(minr1, minc1, maxr1, maxc1), (minr2, minc2, maxr2, maxc2), ... , (minrN, mincN, maxrN, maxcN)]
        """

        if img.dtype != np.uint8:
            raise ValueError('img argument must be of type np.uint8. You can use skimage.util.img_as_ubyte(img)')

        if color is None:
            color = self._get_color(Color.Red)

        else:
            color = self._get_color(color)

        for minr, minc, maxr, maxc in bboxes:
            img[minr, minc:maxc, :] = color # _ (up)
            img[minr:maxr, minc, :] = color # | (left)
            img[maxr, minc:maxc, :] = color # _ (bottom)
            img[minr:maxr, maxc, :] = color # | (right)

    
    def _get_color(self, option):
        if option == Color.Red:
            color = np.array([255, 0, 0], dtype=np.uint8)
        
        elif option == Color.Green:
            color = np.array([0, 255, 0], dtype=np.uint8)

        elif option == Color.Blue:
            color = np.array([0, 0, 255], dtype=np.uint8)

        else:
            color = np.array([0, 0, 0], dtype=np.uint8)
            raise ValueError("color option not supported.'")

        return color


    def linear_interpolation(self, array, limit=None):
        """
        Fill np.nan values using linear interpolation, optionally only fill gaps up to a
        size of limit.
        """
    
        # Indexes of the values to apply interpolation.
        i = np.arange(array.size)

        # an array were values are false for np.nan values and true otherwise.
        valid = np.isfinite(array) 

        filled = np.interp(i, i[valid], array[valid])

        if limit is not None:
            invalid = ~valid
            for n in range(1, limit+1):
                invalid[:-n] &= invalid[n:]
            filled[invalid] = np.nan

        return filled
    