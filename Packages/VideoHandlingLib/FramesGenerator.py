import numpy as np
import av


class FramesGenerator(object):
    """
    Class used for obtaining the frames of a given video.

    FramesGenerator is used for obtaining the frames of a given video.
    It uses the external module PyAv. If you don't have the module,
    you can visit https://github.com/mikeboers/PyAV#installation
    for instructions on how to install it. numpy is also required.
    
    Typical usage example:

    frames_generator = FramesGenerator()
            
    for img in frames_generator.generate_frames():
        # do some operation with the img ...
        pass

    Attributes:
        __video_path: A private attribute string indicating the path to the video.
    """


    def __init__(self, video_path):
        self.__video_path = video_path


    def generate_frames(self, total=None):
        """
        Yields images as a numpy array for a video.
        
        This method is a generator that yields images for each frame
        in a given video specified at the class constructor. Time 
        complexity is O(n) where n is the number of frames in the video.
        Space complexity is constant.

        Typical usage example:
            
        frames_generator = FramesGenerator()
        
        for img in frames_generator.generate_frames():
            # do some operation with the img ...
            pass

        Args:
            total (int): An optional integer indicating how many images to generate from 
            the video starting at frame 0 until total-1.

        Yields:
            Yields an image as a numpy array.

        Raises:
            AVError: Raises an exception if the given path for the video is not found.
        """

        try:
            video = av.open(self.__video_path)

            if total == None:
                for i, frame in enumerate(video.decode(video=0)):
                    img = frame.to_image().convert('RGB')
                    img = np.array(img)
                    yield img

            else:
                for i, frame in enumerate(video.decode(video=0)):
                    if total-1 < i:
                        break
                    img = frame.to_image().convert('RGB')
                    img = np.array(img)
                    yield img
        
        finally:
            video.close()
