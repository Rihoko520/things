import cv2
import numpy as np
from skimage import exposure, img_as_float

def raw():

    img = cv2.imread('detector/combine.png')
    
    if img is None:
        print("Error: Could not read the image.")
    else:
        print("Image loaded successfully.")
        resized_img = cv2.resize(img, (640, 480))
        cv2.imshow('Image', resized_img)
    return resized_img

def img_adjust(img):
    # Load a sample image
    image = img_as_float(img)

    # Adjust gamma
    gamma_corrected = exposure.adjust_gamma(image, gamma=17) #Example: Darkens the image
    
    # Convert the image to a supported data type
    img = gamma_corrected
    if img.dtype == np.float64:
        img = img.astype(np.float32) #Convert to float32 if necessary
        img = (img * 255).astype(np.uint8) #Scale and convert to uint8 if necessary

    cv2.imshow("gamma_corrected", img)
    return img

def gray(img):
    if img is None:
        print("Error: Could not read the image.")
    else:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grayscale Image", img_gray)
    return img_gray

def binary(img):
    ret,thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 显示结果
    cv2.imshow('Binarized Image', thresh)
    return thresh

def put_text(img,color,rect):
    center_x = int(rect[0][0])
    center_y = int(rect[0][1])
    org = (center_x, center_y)  # Bottom-left corner coordinates
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 2

    # Draw the text
    cv2.putText(img,f"({center_x}, {center_y})", org, font, fontScale, color, thickness)


def adjust_rotated_rect(rect):
    c, (w, h), angle = rect
    if w > h:
        w, h = h, w  # Swap width and height
        angle = (angle + 90) % 360 # Add 90 degrees, ensuring angle is between 0 and 360

        # Adjust angle to be between -90 and 90
        if angle > 180:
            angle -= 360 # Adjust to negative angle
        elif angle > 90:
            angle -= 180 # Adjust to negative angle
    rect = c, (w, h), angle
    return rect # Ensure angle is within 0-360 degrees

def is_close(rect1, rect2, angle_tol, height_tol, width_tol, cy_tol):
    """检查两个旋转矩形是否足够接近。"""
    (cx1, cy1), (w1, h1), angle1 = rect1
    (cx2, cy2), (w2, h2), angle2 = rect2

    angle_diff = abs(angle1 - angle2)
    angle_diff = min(angle_diff, 360 - angle_diff)  # 考虑角度环绕
    height_diff = abs(h1 - h2)
    width_diff = abs(w1 - w2)
    cy_diff = abs(cy1 - cy2)

    return (angle_diff <= angle_tol and height_diff <= height_tol and
            width_diff <= width_tol and cy_diff <= cy_tol)

def group_close_rotated_rects(rotated_rects, angle_tol=10, height_tol=10, width_tol=5, cy_tol=100):
    """将距离较近的旋转矩形进行分组，可以找到多组匹配。

    参数：
        rotated_rects: 一个元组列表，每个元组表示一个旋转矩形，格式为 (cx, cy, w, h, angle)。
        angle_tol: 角度容差 (度)。
        height_tol: 高度容差。
        width_tol: 宽度容差。
        cy_tol: 中心点y坐标容差。

    返回：
        一个列表，其中包含多个分组后的旋转矩形列表。每个子列表代表一组匹配的旋转矩形。
    """

    # 复制输入列表，避免修改原始数据
    rects_copy = rotated_rects[:]
    all_groups = []
    
    while rects_copy:
        rect1 = rects_copy.pop(0)  # 从列表中取出一个矩形
        group = [rect1]
        
        # 寻找与rect1匹配的矩形
        i = 0
        while i < len(rects_copy):
            rect2 = rects_copy[i]
            if is_close(rect1, rect2, angle_tol, height_tol, width_tol, cy_tol):
                group.append(rects_copy.pop(i)) #移除已匹配的矩形
            else:
                i += 1

        all_groups.append(group) # 将找到的一组匹配添加到结果列表

    return all_groups

def armortype(img_raw,rotated_rect):
    """
    检测旋转矩形ROI区域的主要颜色,排除黑色。红色为0,蓝色为1。

    参数：
        frame: 输入图像帧。
        rotated_rect: OpenCV RotatedRect 对象，表示旋转矩形。

    返回：
        0: 主要颜色为红色
        1: 主要颜色为蓝色
        -1: 主要颜色为其他颜色或ROI区域无效
    """
    try:
        # 获取旋转矩形的四个顶点
        points = cv2.boxPoints(rotated_rect)
        points = np.int0(points) # 将坐标转换为整数

        # 创建掩码
        mask = np.zeros(img_raw.shape[:2], dtype=np.uint8)
        cv2.fillConvexPoly(mask, points, 255) #填充旋转矩形区域

        # 应用掩码到图像
        masked_roi = cv2.bitwise_and(img_raw, img_raw, mask=mask)

        # 提取ROI区域 (现在是旋转矩形)
        x, y, w, h = cv2.boundingRect(points) # 获取最小外接矩形
        roi = masked_roi[y:y+h, x:x+w]

        # 以下代码与之前版本相同，只是使用了masked_roi
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([140, 255, 255])
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])

        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_black = cv2.inRange(hsv, lower_black, upper_black)

        red_pixels = cv2.countNonZero(mask_red)
        blue_pixels = cv2.countNonZero(mask_blue)
        black_pixels = cv2.countNonZero(mask_black)
        total_pixels = roi.shape[0] * roi.shape[1]

        if total_pixels == 0:
            return -1

        total_non_black = total_pixels - black_pixels
        if total_non_black <= 0:
            return -1

        red_ratio = red_pixels / total_non_black if total_non_black > 0 else 0
        blue_ratio = blue_pixels / total_non_black if total_non_black > 0 else 0

        if red_ratio > blue_ratio and red_ratio > 0.5:
            return 0
        elif blue_ratio > red_ratio and blue_ratio > 0.5:
            return 1
        else:
            return -1

    except Exception as e:
        print(f"处理旋转矩形ROI时发生错误: {e}")
        return -1



def merge_rotated_rects(rotated_rects_list):
    merged_rects = []
    for rect_group in rotated_rects_list:
        if not rect_group:
            continue  # 跳过空子列表
    
        points = []
        for rect in rect_group:
            center, (width, height), angle = rect
            # 计算旋转矩形的四个角点坐标
            box = cv2.boxPoints(((center[0], center[1]), (width, height), angle))
            points.extend(box)

        # 使用cv2.minAreaRect找到最小面积的旋转矩形
        merged_rect = cv2.minAreaRect(np.array(points))
        area = merged_rect[1][0] * merged_rect[1][1] # Calculate area of the merged rectangle

        if area >= 5000: # Check if area is above the threshold
            merged_rects.append(merged_rect)

    return merged_rects

def find_armor():
    # Find contours
    img=raw()
    img_raw=img_adjust(img)
    img_binary=binary(gray(img_raw))
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    min_area = 100  # 最小面积阈值 (像素)

    rotated_rects_raw = [] # 存储检测到的旋转矩形数据
    rotated_rects = [] # 存储检测到的旋转矩形数据
    armor_rects = []
    all_groups = []
    armor_red = []
    armor_blue = []
    color=(0,0,0)
    for contour in contours:
        # 查找最小面积旋转矩形
        rect = cv2.minAreaRect(contour)
        area = rect[1][0] * rect[1][1] # 计算面积
        if area > min_area: # 检查面积是否大于阈值
            box = cv2.boxPoints(rect) # 获取旋转矩形的四个角点
            box = np.int0(box) # 将坐标转换为整数
            #print(box)
            #cv2.drawContours(img, [box], 0, color, 2) # 绘制旋转矩形轮廓
            rotated_rects_raw.append(rect) # 将旋转矩形数据添加到列表中

    # 打印检测到的旋转矩形信息
    for i, rect in enumerate(rotated_rects_raw):
        rect=adjust_rotated_rect(rect)#校正数据
        center, (width, height), angle = rect
        rotated_rects.append(rect) # 将旋转矩形数据添加到列表中

    for i, rect in enumerate(rotated_rects):
        center, (width, height), angle = rect
        #print(f"旋转矩形 {i+1}:")
        #print(f"  中心点: {center}")
        #print(f"  宽度: {width}")
        #print(f"  高度: {height}")
        #print(f"  角度: {angle}")

    all_groups = group_close_rotated_rects(rotated_rects)

    armor_rects = merge_rotated_rects(all_groups)

    for i , armor_rect in enumerate(armor_rects):
        # Draw merged rectangle
        center, (width, height), angle = armor_rect
        box = cv2.boxPoints(((center[0], center[1]), (width, height), angle))
        box = np.int0(box)
        color_result = armortype(img_raw, armor_rect)
        if color_result == 1:
            armor_blue.append(armor_rect)
            color=(255, 0, 0)
            put_text(img,color,rect)
            cv2.drawContours(img, [box], 0, color, 3) 
        elif color_result == 0:
            armor_red.append(armor_rect)
            color=(0, 0, 255)
            put_text(img,color,armor_rect)
            cv2.drawContours(img, [box], 0, color, 3) 
    for i,red in enumerate(armor_red):
        print(f"Red Armor Center: {i+1}:{red}")
    for i,blue in enumerate(armor_blue):    
        print(f"Blue Armor Center:{i+1}:{blue}")
    cv2.imshow("armor", img) # 显示带有轮廓的图像

def destroy():
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":

    find_armor()

    destroy()

