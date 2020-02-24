from time import time
import cv2
from sql import SQLConnection

class Video():
    def __init__(self, f_id):
        db = SQLConnection()
        feed_info = db.get_feed(f_id)
        self.previous_frame = None
        if feed_info:
            self.url = feed_info["url"]
            self.vid_cap = cv2.VideoCapture(self.url)
            self.exist = True
        else:
            self.exist = False
    
    def __del__(self):
        if self.exist:
            self.vid_cap.release()

    def get_frame(self):
        if not self.exist:
            return self.previous_frame
        # d = time()
        # print("starting ")
        # grab image from url
        ret, frame = self.vid_cap.read()
        if not ret:
            return self.previous_frame
        # print("finished reading", time() - d)
        # d = time()
        # convert to jpg
        ret, jpg_image = cv2.imencode('.jpg', frame)
        if not ret:
            return self.previous_frame
        # print("finished encoding", time() - d)
        # d = time()
        # convert to bytes
        jpg_bytes = jpg_image.tobytes()
        self.previous_frame = jpg_bytes
        # print("finished to bytes", time() - d)
        return self.previous_frame