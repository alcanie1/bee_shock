import av
import numpy as np

# Note: As of December 12 2019, h265 is not supported.
_CODEC = 'h264'

# RGB24 means that there will be 8 bits for each color dimension.
_COLOR_SPACE = 'rgb24'

# FPS is set to 30 since the video camera used for the project records at 30 fps it is ideal to keep the same FPS.
_FPS = 30

# 5Mbps is recommended for videos of 720p and 10Mbps for 1080p. 8Mbps is a good in between rate.
_BIT_RATE = 8_000_000 # 8 Mbps


class ImgToVideoConverter(object):
    """
    Class used for creating a video out of images.

    It uses the external module PyAv. If you don't have the module,
    visit https://github.com/mikeboers/PyAV#installation
    for instructions on how to install it. numpy is also required.
    Bit rate: 8 Mbps
    Fps: 30
    color space: rgb24
    Codec: h264
    
    Typical usage example:

    with ImgToVideoConverter('/desired/destination/path') as output_video:

        a_white_image = np.ones((500, 500, 3), dtype=np.uint8) * 255
        output_video.append_img_to_video(a_white_image)
        
    Attributes:
        __output_path (string): A private attribute indicating the path were the video will be stored.
    """

    def __init__(self, path):
        self.__output_path = path
        self.__output = None


    def __enter__(self):
        self.__setup_output_stream()
        return self


    def __exit__(self, exc_type, exc_val, traceback):
        self.__release_resources()


    def __setup_output_stream(self):
        self.__output = av.open(self.__output_path, 'w')
        self.__stream = self.__output.add_stream(_CODEC, _FPS)
        self.__stream.bit_rate = _BIT_RATE


    def __release_resources(self):
        packet = self.__stream.encode(None)
        self.__output.mux(packet) # flush
        self.__output.close()


    def append_img_to_video(self, img):
        """
        Method that inputs an image to the video output stream for the specefied path
        in the constructor.

        Args:
            img: An image as numpy array.

        Returns:
            No value is returned.

        Raises:
            ValueError: Raises an exception if the argument img is not a numpy array.
        """

        if not isinstance(img, np.ndarray):
            raise ValueError("Argument must be of type numpy.ndarray")
        
        img_as_frame = av.VideoFrame.from_ndarray(img, format=_COLOR_SPACE)
        packet = self.__stream.encode(img_as_frame)
        self.__output.mux(packet)
