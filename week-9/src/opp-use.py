import cv2
import numpy as np

class detect:
    def resize(img):
        target_width = 640
        target_height = 480

        # 调整图像大小
        img = cv2.resize(img, (target_width, target_height))
        return img


class square(detect):
    
    #denoise太几把卡了别用
    def denoise(image_path):
        image = cv2.imread(image_path)
        # 消噪
        denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        return denoised_image

    def enhanced_image(denoised_image):     
        # 图像增强和对比度增强
        alpha = 1.0  # 对比度增强参数（默认为1.0）
        beta = 15  # 亮度增强参数
        enhanced_image = cv2.convertScaleAbs(denoised_image, alpha=alpha, beta=beta)
        return enhanced_image
    def contours_detecto(enhanced_image,image_path):
        # 边缘检测
        edges = cv2.Canny(enhanced_image, 50, 150)
        # 查找轮廓
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #新建轮廓列表
        quadrilaterals = []
        for contour in contours:
            # 计算轮廓的面积
            area = cv2.contourArea(contour)
            # 排除面积较小的轮廓
            if area > 2000:
                # 计算轮廓的周长
                perimeter = cv2.arcLength(contour, True)
                # 对轮廓进行多边形逼近
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

                # 如果逼近的轮廓是四边形，将其添加到列表中
                if len(approx) == 4:
                    quadrilaterals.append(approx)
        marked_image = image_path

        for quad in quadrilaterals:
            # 绘制轮廓
            cv2.drawContours(marked_image, [quad], -1, (200, 250, 10), 2)

            # 绘制顶点并标记坐标
            for i, point in enumerate(quad):
                x, y = point[0]
                cv2.circle(marked_image, (x, y), 5, (0, 255, 255), -1)
                cv2.putText(marked_image, f"({x}, {y})", (x, y), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 50, 255), 2)

            # 计算中心点并标记坐标
            M = cv2.moments(quad)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
        
            # 在标记图像上绘制中心点
                cv2.circle(marked_image, (cx, cy), 5, (0, 255, 0), -1)
                cv2.putText(marked_image, f"({cx}, {cy})", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
                print("中心点坐标:", cx, cy)
            else:
                print("Error: m00为0，无法计算中心坐标")
        return marked_image

class color(detect):
    def detectto(image_path):

        image = cv2.imread(image_path)
    
        # 将图像转换为HSV颜色空间
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
        # 定义红色和绿色的HSV范围
        lower_red = np.array([170, 167, 92])  
        upper_red = np.array([176, 236, 162])  
        lower_green = np.array([57, 129, 86])  
        upper_green = np.array([83, 183, 193]) 

        # 根据颜色范围创建掩模
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        # 使用形态学操作对掩膜进行处理，去除噪音
        kernel = np.ones((5,5),np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    
        # 寻找红色点的轮廓
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 寻找绿色点的轮廓
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 遍历红色点的轮廓
        for contour in contours_red:
            # 获取红色点的坐标
            #（x，y）为轮廓最左边的坐标
            #z为x向右移z个单位（即是轮廓的宽）
            #k为y向下移k个单位（即是轮廓的高）
            x, y, z, k = cv2.boundingRect(contour)
            # 在图像上绘制红色边界框
            cv2.rectangle(image, (x, y), (x+z, y+k), (0, 0, 255), 2)
            # 在图像上标出绿色区域的中心坐标
            cv2.putText(image, f'Red: ({x + z // 2}, {y + k // 2})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("红色点坐标:", x + z // 2, y + k // 2)

        # 遍历绿色点的轮廓
        for contour in contours_green:
            # 获取绿色点的坐标
            #（x，y）为轮廓最左边的坐标
            #z为x向右移z个单位（即是轮廓的宽）
            #k为y向下移k个单位（即是轮廓的高）
            x, y, z, k = cv2.boundingRect(contour)
            # 在图像上绘制绿色边界框
            cv2.rectangle(image, (x, y), (x+z, y+k), (0, 255, 0), 2)
            # 在图像上标出绿色区域的中心坐标
            cv2.putText(image, f'Green: ({x + z // 2}, {y + k // 2})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print("绿色点坐标:", x + z // 2, y + k // 2)
        # 返回图像
        return image
    
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
        url='http://192.168.1.144:4747/video/'
        video_stream = cv2.VideoCapture(url)
        while True:  
            ret, frame = video_stream.read()
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
    url='http://192.168.1.209:4747/video/'
    video_stream = cv2.VideoCapture(url)
    while True:
        ret, frame = video_stream.read()
        
        # 检查图像是否成功读取
        if not ret:
            print("Error: Failed to read frame")
            break
        save_path = 'frame.jpg'
        cv2.imwrite(save_path, frame) 
        save_path = cv2.imread(save_path)
        enhanced_image = square.enhanced_image(save_path)
        contours_detecto = square.contours_detecto(enhanced_image,save_path)
        cv2.imshow('frame', contours_detecto)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    video_stream.release()
    cv2.destroyAllWindows()