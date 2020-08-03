from skimage import color, measure
import scipy.ndimage as ndi
import numpy as np


class BeeSegmenter(object):

    def power_is_on(self, img):
        # 50,000 is the threshold of pixels that are close to black in
        # the red channel
        threshold = 50_000
        red_chan = img[...,0]
        freq, _ = np.histogram(np.ravel(red_chan))

        if freq[0] >= threshold:
            return False

        else:
            return True


    def segment_bees(self, img):
        mask = self.compute_mask(img)
        labeled_bees = self.label_bees(mask)
        bboxes = self.get_bounding_boxes(labeled_bees)
        return bboxes


    def compute_mask(self, img):
        img = color.rgb2hsv(img)
        return (img[...,0] <= 0.25) & (img[...,2] <= 0.4)


    def label_bees(self, mask):
        mask = ndi.median_filter(mask, size=9)
        return measure.label(mask)


    def get_bounding_boxes(self, labeled_bees):

        bboxes = []
        for region in measure.regionprops(labeled_bees):
            
            if region.area >= 110:
                min_row, min_col, max_row, max_col = region.bbox
                bboxes.append([min_row, min_col, max_row, max_col])
        
        return bboxes

    
    def get_bee_positions(self, bboxes):
        detected_bees_coords = self.__get_coords(bboxes)

        # Note: bees_y_axis_vals[i] might contain np.nan values if bee i was not detected. 
        bees_y_axis_vals = self.__match_bees_with_corresponding_coords(detected_bees_coords)
        return bees_y_axis_vals


    def __get_coords(self, bboxes):
        detected_bees_count = len(bboxes)
        # detected_bees_coords = np.full(detected_bees_count, (0,0))
        detected_bees_coords = []

        # i = 0
        for min_row, min_col, max_row, max_col in bboxes:
            x = (max_col + min_col) // 2
            y = (max_row + min_row) // 2
            # detected_bees_coords[i] = (x, y)
            detected_bees_coords.append((x, y))
            # i += 1

        return detected_bees_coords


    def __match_bees_with_corresponding_coords(self, detected_bees_coords):
        # BEE_RANGES[0] is the Cell 1 in the image (The one without a bee) and its pair values are (x1, x2)
        BEE_RANGES = self.__get_bees_ranges()

        # Splits the yellow and the blue areas in the video.
        # HEIGHT = 150

        bees_y_axis_values = np.full(10, np.nan)

        # It will iterate at most 100 times. 
        for x, y in detected_bees_coords:
            for i, xs in enumerate(BEE_RANGES):

                x1, x2 = xs[0], xs[1]
                
                # It will only enter this if block 
                # if the bee located between x1 and x2 was detected.

                if x1 < x and x < x2:
                    bees_y_axis_values[i] = y

        ''' ** Note: bees_y_axis_values[i] might contain np.nan values if bee i was not detected. ** '''

        return bees_y_axis_values

    
    def __get_bees_ranges(self):
        # bees pixels ranges. The first bee is located between pixels 0 to 51 in the horizontal axis.
        BEE1_RANGE, BEE2_RANGE, BEE3_RANGE = [0, 51], [51, 110], [110, 160]
        BEE4_RANGE, BEE5_RANGE, BEE6_RANGE = [160, 210], [210, 270], [270, 320]
        BEE7_RANGE, BEE8_RANGE, BEE9_RANGE = [320, 380], [380, 430], [430, 490]
        BEE10_RANGE = [490, 540]

        BEE_RANGES = np.array([
            np.array(BEE1_RANGE), np.array(BEE2_RANGE), np.array(BEE3_RANGE), 
            np.array(BEE4_RANGE),np.array(BEE5_RANGE), np.array(BEE6_RANGE), 
            np.array(BEE7_RANGE), np.array(BEE8_RANGE),np.array(BEE9_RANGE),
            np.array(BEE10_RANGE)
        ])

        return BEE_RANGES
                    