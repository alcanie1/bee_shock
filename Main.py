from Packages.VideoHandlingLib import FramesGenerator, ImgToVideoConverter
from Packages.BeeShockLib import ImgManipulator, BeeSegmenter, Color, BeeStatistics
from config import *
from skimage.util import img_as_ubyte
import numpy as np


bees_positions = np.array([
    np.zeros(TOTAL_FRAMES), np.zeros(TOTAL_FRAMES), np.zeros(TOTAL_FRAMES), np.zeros(TOTAL_FRAMES), np.zeros(TOTAL_FRAMES),
    np.zeros(TOTAL_FRAMES), np.zeros(TOTAL_FRAMES), np.zeros(TOTAL_FRAMES), np.zeros(TOTAL_FRAMES), np.zeros(TOTAL_FRAMES) 
])


def main():
    
    with ImgToVideoConverter(VIDEO_DST_PATH) as output_video:
        
        img_manipulator = ImgManipulator()
        bee_segmenter = BeeSegmenter()
        frames_generator = FramesGenerator(VIDEO_SRC_PATH)

        frame_number = 0
        for img in frames_generator.generate_frames(total=TOTAL_FRAMES):

            print(f'Processing frame {frame_number} ...')

            if bee_segmenter.power_is_on(img):

                # Prepare image for segmentation.
                img = img_manipulator.projective_transform(img, output_shape=(325, 640)) 
                img = img_manipulator.crop(img, x_range=(50, 610), y_range=(0, 315))
            
                # Segment bees and draw bounding boxes around them.
                img = img_as_ubyte(img)
                bounding_boxes = bee_segmenter.segment_bees(img)
                img_manipulator.add_bounding_boxes(img, bounding_boxes, color=Color.Red)

                # Add the image to the video.
                output_video.append_img_to_video(img)

                # Note: Undetected bees will contain np.nan in their y values.
                bees_y_axis_vals = bee_segmenter.get_bee_positions(bounding_boxes)
                
                # Store the position in the corresponding bees_positions index for future data visualization.
                for corresponding_bee_index, position in enumerate(bees_y_axis_vals):
                    bees_positions[corresponding_bee_index][frame_number] = position


            # It wont enter this else block after the frame 176.
            else:
                # transform and crop the image before appending to video so
                # it matches the angles and sizes of the ones processed in 
                # the block above.
                img = img_manipulator.projective_transform(img, output_shape=(325, 640)) 
                img = img_manipulator.crop(img, x_range=(50, 610), y_range=(0, 315))
                img = img_as_ubyte(img)
                output_video.append_img_to_video(img)
            
            frame_number += 1
    
    print('Aproximating NaN values with linear interpolation ...')
    for i, bee_positions in enumerate(bees_positions):
        # Apply linear interpolation to up to 3 nan values in a row.
        bees_positions[i] = img_manipulator.linear_interpolation(bee_positions, limit=3)

    bee_statistics = BeeStatistics()

    print(f'Saving graph figures at {GRAPH_DST_PATH} ...')
    bee_statistics.graph_bees_positions(bees_positions, GRAPH_DST_PATH)

    print(f'Saving statistics at {STATS_DST_PATH} ...')
    bee_statistics.compute_bee_statistics(bees_positions, STATS_DST_PATH)

    print('Done.')
    

if __name__ == '__main__':
    main()
