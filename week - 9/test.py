import cv2
import numpy as np

# 读取图像
image = cv2.imread('photo/1.jpg')

# 将图像转换为灰度
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 应用Canny边缘检测
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# 在边缘图像中查找轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 定义轮廓的最小和最大面积阈值
min_area =7500
max_area = 8000
# 遍历轮廓
for contour in contours:
    # 计算轮廓的面积
    area = cv2.contourArea(contour)

    # 如果轮廓的面积在指定范围内
    if min_area < area < max_area:
    # 将轮廓逼近为多边形
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

    # 如果轮廓有4个角点，则可能是矩形
        if len(approx) == 4:
        # 在图像上绘制矩形
            cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)

            # 获取矩形的坐标
            x, y, w, h = cv2.boundingRect(approx)
            x2, y2 = x + w, y + h
        
            # 计算矩形的中点坐标
            center_x = (x + x2) // 2
            center_y = (y + y2) // 2

            # 打印矩形的中点坐标
            print("矩形中点坐标:", center_x, center_y)

            # 在图像上绘制中点
            cv2.circle(image, (center_x, center_y), 5, (255, 0, 0), -1)

            # 打印矩形的坐标
            print("矩形左上角坐标:", x, y)
            print("矩形右下角坐标:", x2, y2)

# 对边缘图像进行膨胀操作
kernel = np.ones((5, 5), np.uint8)
dilated_edges = cv2.dilate(edges, kernel, iterations=1)

# 在膨胀后的边缘图像中查找轮廓
contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 遍历轮廓
for contour in contours:
    # 将轮廓逼近为多边形
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # 如果轮廓有4个角点，则可能是矩形
    if len(approx) == 4:
        # 在图像上绘制矩形
        cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)

        # 获取矩形的坐标
        x, y, w, h = cv2.boundingRect(approx)
        x2, y2 = x + w, y + h
        
        # 计算矩形的中点坐标
        center_x = (x + x2) // 2
        center_y = (y + y2) // 2

        # 打印矩形的中点坐标
        print("矩形中点坐标:", center_x, center_y)

        # 在图像上绘制中点
        cv2.circle(image, (center_x, center_y), 5, (255, 0, 0), -1)

        # 打印矩形的坐标
        print("矩形左上角坐标:", x, y)
        print("矩形右下角坐标:", x2, y2)

# 显示带有检测到的矩形的图像
cv2.imshow('检测到的矩形', image)

# 读取图像
image = cv2.imread('photo/1.jpg')

# 将图像转换为HSV颜色空间
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 定义红色和绿色的HSV范围
# red(160-180 or 0-10)
lower_red = np.array([160, 100, 100])
upper_red = np.array([180, 255, 255])

lower_green = np.array([40, 40, 40])
upper_green = np.array([80, 255, 255])

# 根据颜色范围创建掩模
mask_red = cv2.inRange(hsv, lower_red, upper_red)
mask_green = cv2.inRange(hsv, lower_green, upper_green)

# 寻找红色点的轮廓
contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 寻找绿色点的轮廓
contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 遍历红色点的轮廓
for contour in contours_red:
    # 获取红色点的坐标
    M = cv2.moments(contour)
    red_center_x = int(M["m10"] / M["m00"])
    red_center_y = int(M["m01"] / M["m00"])
    print("红色点坐标:", red_center_x, red_center_y)

# 遍历绿色点的轮廓
for contour in contours_green:
    # 获取绿色点的坐标
    M = cv2.moments(contour)
    green_center_x = int(M["m10"] / M["m00"])
    green_center_y = int(M["m01"] / M["m00"])
    print("绿色点坐标:", green_center_x, green_center_y)

# 在图像上绘制红色点和绿色点
image_red = cv2.bitwise_and(image, image, mask=mask_red)
image_green = cv2.bitwise_and(image, image, mask=mask_green)

# 显示带有红色点和绿色点的图像
cv2.imshow('红色点', image_red)
cv2.imshow('绿色点', image_green)
cv2.waitKey(0)
cv2.destroyAllWindows()