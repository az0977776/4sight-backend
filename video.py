from time import time
import cv2
from sql import SQLConnection

class Video():
    def __init__(self, f_id):
        db = SQLConnection()
        feed_info = db.get_feed(f_id)
        
        self.previous_frame = None
        self.url = feed_info["url"]
        self.vid_cap = cv2.VideoCapture(self.url)
        # self.vid_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.vid_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        # self.vid_cap.set(cv2.CAP_PROP_FPS, 1)
        # print(self.vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # print(self.vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # print(self.vid_cap.get(cv2.CAP_PROP_FPS))
    
    def __del__(self):
        self.vid_cap.release()

    def get_frame(self):
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