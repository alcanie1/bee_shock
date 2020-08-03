import av
from skimage import io

container = av.open('video_footage.mp4')

for packet in container.demux():
    for frame in packet.decode():
        if frame.type == 'video':
            img = frame.to_image()  # PIL/Pillow image
            arr = np.asarray(img)  # numpy array
            io.imsave(f'{frame}.jpeg')

            
            for packet in container.demux():
    for frame in packet.decode():
        if frame.type == 'video':
            img = frame.to_image()  # PIL/Pillow image
            arr = np.asarray(img)  # numpy array
            # Do something!