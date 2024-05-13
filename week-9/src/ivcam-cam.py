import cv2
import numpy as np
from cam import calculate_intersection,shrink_rectangle,average_points,draw_line_points,pre_cut,preprocess_image,find_max_perimeter_contour,roi_cut,find_point,draw_point,draw_contour_and_vertices,persp_trans,draw_warped_image,shrink_rectangle_new,inv_trans_vertices
from typing import List




if __name__ == "__main__":
    video_stream = cv2.VideoCapture(0)
    while True:
        ret, frame = video_stream.read()
        
        # 检查图像是否成功读取
        if not ret:
            print("Error: Failed to read frame")
            break
        save_path = 'frame.jpg'
        cv2.imwrite(save_path, frame)
        # 读取图像
        img = cv2.imread(save_path)
    
        # 预处理图像，获取轮廓
        contours = preprocess_image(img)

        # 如果轮廓不为空，则寻找具有最大周长的矩形
        if contours is not None:
            vertices = find_max_perimeter_contour(contours, 10090*4, 200*4)
        
        # 如果找到了轮廓的顶点，则进行ROI切割，并寻找红点和绿点
        if vertices is not None:
            
           # 根据顶点进行ROI区域切割
            roi_img = roi_cut(img, vertices)

            # 在ROI图像中寻找红点和绿点
            red_point, green_point = find_point(roi_img)
        
            # 如果找到红点，则在原图上标注红点
            if red_point is not None:
                draw_point(img, red_point, color = 'red ')
        
            # 如果找到绿点，则在原图上标注绿点
            if green_point is not None:
                draw_point(img, green_point, color = 'green ')

            # 在原图上绘制轮廓和顶点
            img, _ = draw_contour_and_vertices(img, vertices, (5/6))  # 绘制轮廓和顶点，调整比例因子

        # 显示处理后的图像
        cv2.imshow("final", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    video_stream.release()
    cv2.destroyAllWindows()