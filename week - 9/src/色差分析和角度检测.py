#该代码应插入到for循环中进行使用(for contour in contours:)
# 如果轮廓有4个角点，则可能是矩形
if len(approx) == 4:
        # 计算四边形的内部角度
        angles = []
        for i in range(4):
            pt1 = approx[i][0]
            pt2 = approx[(i + 1) % 4][0]
            pt3 = approx[(i + 2) % 4][0]
            angle = np.degrees(np.arctan2(pt3[1] - pt2[1], pt3[0] - pt2[0]) - np.arctan2(pt1[1] - pt2[1], pt1[0] - pt2[0]))
            angles.append(angle)

# 检查角度是否符合条件
            if all(angle >= 80 and angle <= 140 for angle in angles):
                for cnt in contours:
                # 计算每个轮廓的颜色均值
                    mask = np.zeros(gray.shape, np.uint8)
                    cv2.drawContours(mask, [cnt], -1, 255, -1)
                    mean_val = cv2.mean(image, mask=mask)
# 根据颜色均值判断色差大小
# 这里可以根据实际情况定义色差的阈值
                    if mean_val[0] < 100 and mean_val[1] < 100 and mean_val[2] < 100:
# 绘制或保留色差较小的轮廓
                        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
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
