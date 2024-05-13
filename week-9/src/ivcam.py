import cv2
import numpy as np
from red_green_detect import detectto 
from square_detect import  enhanced_image, contours_detecto,square
from Findhsv import find


def findred_green(frame):
    find(frame)

        
def adjustfindcolor():
    video_stream = cv2.VideoCapture(0)
    while True:
        ret, frame = video_stream.read()
        
        # 检查图像是否成功读取
        if not ret:
            print("Error: Failed to read frame")
            break


        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    video_stream.release()
    cv2.destroyAllWindows()
    find(frame)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    url='http://192.168.1.144:4747/video/'
    video_stream = cv2.VideoCapture(url)
    while True:
        ret, frame = video_stream.read()
        
        # 检查图像是否成功读取
        if not ret:
            print("Error: Failed to read frame")
            break
        save_path = 'frame.jpg'
        cv2.imwrite(save_path, frame) 
        frame = square(save_path)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    video_stream.release()
    cv2.destroyAllWindows()