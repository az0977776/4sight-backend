from time import time
import cv2

video_url = {
    '0':"http://32.208.120.218/mjpg/video.mjpg",
    '1':"http://81.14.37.24:8080/mjpg/video.mjpg",
    '2':"http://87.139.9.247/mjpg/video.mjpg",
    '3':"http://220.240.123.205/mjpg/video.mjpg",
    '4':"http://89.29.108.38/mjpg/video.mjpg",
    '5':"http://166.130.18.45:1024/mjpg/video.mjpg"
}


class Video():
    def __init__(self, vid):
        self.previous_frame = None
        self.url = video_url[vid]
        self.vid_cap = cv2.VideoCapture(self.url)
        # self.vid_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
        # self.vid_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
        # self.vid_cap.set(cv2.CAP_PROP_FPS, 1)
    
    def __del__(self):
        self.vid_cap.release()

    def get_frame(self):
        d = time()
        print("starting ")
        # grab image from url
        ret, frame = self.vid_cap.read()
        if not ret:
            return self.previous_frame
        print("finished reading", time() - d)
        d = time()
        # convert to jpg
        ret, jpg_image = cv2.imencode('.jpg', frame)
        if not ret:
            return self.previous_frame
        print("finished encoding", time() - d)
        d = time()
        # convert to bytes
        jpg_bytes = jpg_image.tobytes()
        self.previous_frame = jpg_bytes
        print("finished to bytes", time() - d)
        return self.previous_frame