import numpy as np
import cv2

cap = cv2.VideoCapture("http://32.208.120.218/mjpg/video.mjpg")
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"width:{width} height:{height} fps:{fps}")

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'jpeg')
out = cv2.VideoWriter('output.avi', fourcc, 1, (height, width))

while(cap.isOpened()):
    print("reading")
    ret, frame = cap.read()
    if not ret:
        break

    # write the flipped frame
    out.write(frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(-1) & 0xFF == ord('q'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
