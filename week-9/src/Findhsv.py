import cv2  
import numpy as np  

def find():  
  
    # 初始化HSV范围  
    h_min, s_min, v_min = 0, 100, 100  
    h_max, s_max, v_max = 10, 255, 255  
  
    # 创建窗口  
    cv2.namedWindow('Color Thresholding')  
  
    # 创建滑动条  
    cv2.createTrackbar('H_min', 'Color Thresholding', h_min, 255, lambda x: None)  
    cv2.createTrackbar('S_min', 'Color Thresholding', s_min, 255, lambda x: None)  
    cv2.createTrackbar('V_min', 'Color Thresholding', v_min, 255, lambda x: None)  
    cv2.createTrackbar('H_max', 'Color Thresholding', h_max, 255, lambda x: None)  
    cv2.createTrackbar('S_max', 'Color Thresholding', s_max, 255, lambda x: None)  
    cv2.createTrackbar('V_max', 'Color Thresholding', v_max, 255, lambda x: None)  
    url='http://192.168.1.209:4747/video/'
    video_stream = cv2.VideoCapture(url)
    while True:  
        ret, frame = video_stream.read(0)
        # 转换到HSV颜色空间  
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
        # 获取滑动条的值  
        h_min = cv2.getTrackbarPos('H_min', 'Color Thresholding')  
        s_min = cv2.getTrackbarPos('S_min', 'Color Thresholding')  
        v_min = cv2.getTrackbarPos('V_min', 'Color Thresholding')  
        h_max = cv2.getTrackbarPos('H_max', 'Color Thresholding')  
        s_max = cv2.getTrackbarPos('S_max', 'Color Thresholding')  
        v_max = cv2.getTrackbarPos('V_max', 'Color Thresholding')  
      
        # 应用inRange函数创建掩模  
        lower_color = np.array([h_min, s_min, v_min])  
        upper_color = np.array([h_max, s_max, v_max])  
        mask_red = cv2.inRange(hsv, lower_color, upper_color)  
      
        # 创建一个结果图像来可视化掩模  
        result = cv2.bitwise_and(frame, frame, mask=mask_red)  
      
        # 显示结果图像  
        cv2.imshow('Color Thresholding', result)  
      
        # 等待按键，如果按下'q'则退出循环  
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break  

if __name__ == "__main__":
    
    find()   
    # 销毁所有窗口  
    cv2.destroyAllWindows()