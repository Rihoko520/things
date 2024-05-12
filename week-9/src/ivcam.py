def denoise(image_path):
    image = cv2.imread(image_path)
    # 消噪
    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    return denoised_image


def enhanced_image(denoised_image):     
    # 图像增强和对比度增强
    alpha = 1.5  # 对比度增强参数（默认为1.0）
    beta = 15  # 亮度增强参数
    enhanced_image = cv2.convertScaleAbs(denoised_image, alpha=alpha, beta=beta)
    return enhanced_image


def contours_detecto(enhanced_image):
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
    image = cv2.imread(image)
    marked_image = image.copy()

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
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    cv2.circle(marked_image, (cx, cy), 5, (0, 255, 0), -1)
    cv2.putText(marked_image, f"({cx}, {cy})", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    print("中心点坐标:", cx, cy)
    return marked_image



def detectto(image_path):

    image = cv2.imread(image_path)
    
    # 将图像转换为HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 定义红色和绿色的HSV范围
    lower_red = np.array([165, 100, 100])
    upper_red = np.array([179, 255, 255])

    lower_green = np.array([36, 100, 100])
    upper_green = np.array([86, 255, 255])

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

import cv2

# 替换IP_ADDRESS为iVCam所在设备的IP地址
url = "198.18.0.1"


# 从iVCam设备捕获视频流
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("无法捕获视频流")
        break

    # 在窗口中显示视频流
    cv2.imshow('video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # 释放视频资源
cv2.destroyAllWindows()  # 释放窗口资源