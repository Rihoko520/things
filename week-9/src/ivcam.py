import cv2
import numpy as np
from red_green_detect import detectto 
from square_detect import denoise, enhanced_image, contours_detecto
from Findhsv import find
    
def all(frame):
    save_path = 'frame.jpg'
    cv2.imwrite(save_path, frame) 
    # 图像处理步骤
    denoised_ = denoise(save_path)
    enhanced_ = enhanced_image(denoised_)
    final_ = contours_detecto(enhanced_,frame)

    image = detectto(save_path)

    # 合并图像
    Final_image = cv2.addWeighted(image, 0.6, final_, 0.6, 0)
        
    frame_rgb = cv2.cvtColor(Final_image, cv2.COLOR_BGR2RGB)
    return frame_rgb

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
    video_stream = cv2.VideoCapture(0)
    while True:
        ret, frame = video_stream.read()
        
        # 检查图像是否成功读取
        if not ret:
            print("Error: Failed to read frame")
            break
        frame = all(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    video_stream.release()
    cv2.destroyAllWindows()