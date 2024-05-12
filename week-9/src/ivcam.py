import cv2
import numpy as np
from red_green_detect import detectto 
from square_detect import  denoise,enhanced_image,contours_detecto


# 替换IP_ADDRESS为iVCam所在设备的IP地址
url = "rtmp://198.18.0.1:19351"

import IPython.display as ipythondisplay
from IPython.display import display

def show_camera():
    video_stream = cv2.VideoCapture(0)
    while True:
        ret, frame = video_stream.read()
        _, jpeg = cv2.imencode('.jpg', frame)
        display(ipythondisplay.Image(data=jpeg.tobytes()))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_stream.release()
    cv2.destroyAllWindows()

show_camera()