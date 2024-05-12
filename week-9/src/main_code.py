import cv2
import numpy as np
from red_green_detect import detectto 
from square_detect import  denoise,enhanced_image,contours_detecto
from safe import safe_1,win_safe_,linux_safe_
if __name__ == "__main__":
    #获取图片位置
    #原图片名字(可通过直接该project的名字来选定图片直接进行处理)
    project = '1'
    
    image_path = f'{project}.jpg'
    image = cv2.imread(image_path)
    denoised_ = denoise(image_path)
    enhanced_ = enhanced_image(denoised_)
    final_ = contours_detecto(enhanced_,image)
    #处理后的图像文件名
    name ='square'
    safe_1(final_,name)
    win_safe_(name,project)


    image = detectto(image_path)
    #原图像文件名
    name ='color'
    safe_1(image,name)
    win_safe_(name,project)

    #合并图像
    name ='combined'
    Final_image = cv2.addWeighted(image, 0.6, final_, 0.6, 0)
    safe_1(Final_image,name)
    win_safe_(name,project)
    # 显示合并图像
    cv2.namedWindow('combined', cv2.WINDOW_NORMAL)
    cv2.imshow('combined', Final_image)    

    cv2.waitKey(0)
    cv2.destroyAllWindows()