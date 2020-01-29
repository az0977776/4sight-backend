from time import time
import cv2

class Video():
    def __init__(self):
        self.previous_frame = None
        self.url = "http://129.10.161.241/mjpg/video.mjpg"

    def get_frame(self):
        # grab image from url
        cap = cv2.VideoCapture(self.url)
        ret, frame = cap.read()
        if not ret:
            return self.previous_frame
        # convert to jpg
        ret, jpg_image = cv2.imencode('.jpg', frame)
        if not ret:
            return self.previous_frame
        # convert to bytes
        jpg_bytes = jpg_image.tobytes()
        self.previous_frame = jpg_bytes
        return self.previous_frame