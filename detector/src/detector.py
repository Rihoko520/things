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
        #cv2.imshow('Image', resized_img)
    return resized_img

def img_adjust(img):
    # Load a sample image
    image = img_as_float(img)

    # Adjust gamma
    gamma_corrected = exposure.adjust_gamma(image, gamma=30) #Example: Darkens the image
    blur = cv2.GaussianBlur(gamma_corrected, (23, 31), 0)  # 高斯滤波去噪
    #cv2.imshow('Binarized Image', blur)
    # Convert the image to a supported data type
    img = blur
    if img.dtype == np.float64:
        img = img.astype(np.float32) #Convert to float32 if necessary
        img = (img * 255).astype(np.uint8) #Scale and convert to uint8 if necessary

    #cv2.imshow("gamma_corrected", img)
    return img

def gray(img):
    if img is None:
        print("Error: Could not read the image.")
    else:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Grayscale Image", img_gray)
    return img_gray

def binary(img):
    ret,thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 显示结果
    #cv2.imshow('Binarized Image', thresh)
    return thresh

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

def group_close_rotated_rects(rotated_rects, angle_tol=10, height_tol=100, width_tol=50, cy_tol=100):
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

        if area >= 2000 : # Check if area is above the threshold
            if width/height<=3 and width/height>=0 :
                merged_rects.append(merged_rect)

    return merged_rects

def armortype(img_raw, rotated_rect):
    """
    Detects the dominant color (red or blue) within a rotated rectangular ROI, excluding black.

    Args:
        img_raw: Input image frame (BGR).
        rotated_rect: OpenCV RotatedRect object representing the rotated rectangle.

    Returns:
        0: Dominant color is red.
        1: Dominant color is blue.
        -1: Dominant color is neither red nor blue, or ROI is invalid.
    """
    try:
        # Get rotated rectangle points and create a mask
        points = np.int0(cv2.boxPoints(rotated_rect))
        mask = np.zeros_like(img_raw[:,:,0], dtype=np.uint8) #More efficient mask creation
        cv2.fillConvexPoly(mask, points, 255)

        # Apply mask and get ROI
        masked_roi = cv2.bitwise_and(img_raw, img_raw, mask=mask)
        x, y, w, h = cv2.boundingRect(points)
        roi = masked_roi[y:y+h, x:x+w]

        # Convert to HSV and define color ranges (improved blue range)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 43, 46])
        upper_red = np.array([10, 255, 255])
        lower_red_upper = np.array([160, 100, 100])
        upper_red_upper = np.array([180, 255, 255])

        lower_blue = np.array([100, 43, 46]) # Widened range for better blue detection
        upper_blue = np.array([124, 255, 255]) # Widened range for better blue detection

        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])

        #Efficient mask creation using numpy
        mask_red = cv2.inRange(hsv, lower_red, upper_red) | cv2.inRange(hsv, lower_red_upper, upper_red_upper)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_black = cv2.inRange(hsv, lower_black, upper_black)

        # Count non-zero pixels (more efficient)
        red_pixels = np.count_nonzero(mask_red)
        blue_pixels = np.count_nonzero(mask_blue)
        black_pixels = np.count_nonzero(mask_black)
        total_pixels = roi.size // 3 #Efficient total pixel calculation

        #Handle edge cases efficiently
        if total_pixels == 0:
            return -1
        total_non_black = total_pixels - black_pixels
        if total_non_black <= 0: 
            return -1

        red_ratio = red_pixels / total_non_black
        blue_ratio = blue_pixels / total_non_black

        # Determine dominant color
        if red_ratio > blue_ratio and red_ratio > 0.5:
            return 0
        elif blue_ratio > red_ratio and blue_ratio > 0.5:
            return 1
        else:
            return -1

    except Exception as e:
        print(f"Error detecting armor: {e}")
        return -1

def invert_color_loop(rgb):
    """使用循环反转 RGB 颜色元组。

    参数：
     rgb: 表示 RGB 颜色的元组 (例如，(255, 0, 0))。

    返回：
     表示反转后 RGB 颜色的元组。如果输入无效，则返回 None。

    """
    if not isinstance(rgb, tuple) or len(rgb) != 3:
        return None
    inverted = []
    for c in rgb:
        inverted.append(255 - c)
    return tuple(inverted)

def put_text(img,color,rect):
    color=invert_color_loop(color)
    center_x = int(rect[0][0])
    center_y = int(rect[0][1])
    org = (center_x, center_y)  # Bottom-left corner coordinates
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 2

    # Draw the text
    cv2.putText(img,f"({center_x}, {center_y})", org, font, fontScale, color, thickness)

def int_(armor):
    aromor_int_rounded = []
    for outer_tuple in armor:
        new_outer_tuple = []
        for inner_tuple_or_float in outer_tuple:
            if isinstance(inner_tuple_or_float, tuple):
                new_inner_tuple = tuple(int(round(x)) for x in inner_tuple_or_float)
                new_outer_tuple.append(new_inner_tuple)
            else:
                new_outer_tuple.append(int(round(inner_tuple_or_float)))
        aromor_int_rounded.append(tuple(new_outer_tuple))
    return aromor_int_rounded


def find_armor(img):
    armors_dict = {}
    armors_data = []
    rotated_rects_raw = [] # 存储检测到的旋转矩形数据
    rotated_rects = [] # 存储检测到的旋转矩形数据
    armor_rects_raw = []
    armor_rects = []
    all_groups = []
    color=(0,0,0)
    # Find contours
    img_raw=img_adjust(img)
    img_binary=binary(gray(img_raw))
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    min_area = 200  # 最小面积阈值 (像素)

    for contour in contours:
        # 查找最小面积旋转矩形
        rect = cv2.minAreaRect(contour)
        area = rect[1][0] * rect[1][1] # 计算面积
        if area > min_area: # 检查面积是否大于阈值
            box = cv2.boxPoints(rect) # 获取旋转矩形的四个角点
            box = np.int0(box) # 将坐标转换为整数
            #print(box)
            cv2.drawContours(img, [box], 0, color, 2) # 绘制旋转矩形轮廓
            rotated_rects_raw.append(rect) # 将旋转矩形数据添加到列表中

    # 打印检测到的旋转矩形信息
    for i, rect in enumerate(rotated_rects_raw):
        rect = adjust_rotated_rect(rect)#校正数据
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

    armor_rects_raw = merge_rotated_rects(all_groups)
    
    for i, armor_rect_raw in enumerate(armor_rects_raw):
        armor_rect_raw = adjust_rotated_rect(armor_rect_raw)#校正数据
        armor_rects.append(armor_rect_raw) # 将旋转矩形数据添加到列表中
        armor_rects=int_(armor_rects)
        
    for i , armor_rect in enumerate(armor_rects):
        # Draw merged rectangle
        center, (width, height), angle = armor_rect
        box = cv2.boxPoints(((center[0], center[1]), (width, height), angle))
        box = np.int0(box)
        color_result = armortype(img_raw, armor_rect)
        if color_result == 1:
            armors_data = [(f"{center[0]}",{"class_id": 1, "height": height, "center": [center[0], center[1]]})]
            for key, value in armors_data:
                armors_dict[key] = value
            color=(255, 0, 0)
            cv2.drawContours(img, [box], 0, color, 3) 
            put_text(img,color,armor_rect)

        elif color_result == 0:
            armors_data = [(f"{center[0]}",{"class_id": 7, "height": height, "center": [center[0], center[1]]})]
            for key, value in armors_data:
                armors_dict[key] = value
            color=(0, 0, 255)
            cv2.drawContours(img, [box], 0, color, 3) 
            put_text(img,color,armor_rect)

    print(armors_dict)
    cv2.imshow("armor", img) # 显示带有轮廓的图像

def destroy():
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    img=raw()
    find_armor(img)
    destroy()

