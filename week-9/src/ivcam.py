import cv2
import numpy as np
from red_green_detect import detectto 
from square_detect import denoise, enhanced_image, contours_detecto

def show_camera():
    video_stream = cv2.VideoCapture(0)
    while True:
        ret, frame = video_stream.read()
        
        # 检查图像是否成功读取
        if not ret:
            print("Error: Failed to read frame")
            break
        
        # 将图像转换为RGB颜色空间
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        save_path = '15.jpg'
        cv2.imwrite(save_path, frame_rgb) 
        # 图像处理步骤
        denoised_ = denoise(save_path)
        enhanced_ = enhanced_image(denoised_)
        final_ = contours_detecto(enhanced_, frame_rgb)

        image = detectto(save_path)

        # 合并图像
        Final_image = cv2.addWeighted(image, 0.6, final_, 0.6, 0)
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 显示图像
        cv2.imshow('frame', Final_image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_camera()