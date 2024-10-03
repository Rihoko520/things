import cv2
import numpy as np
from skimage import exposure, img_as_float
def adjust_rotated_rect(rect):
    c, (w, h), angle = rect
    if w > h:
        w, h = h, w
        angle = (angle + 90) % 360
        if angle > 180:
            angle -= 360
        elif angle > 90:
            angle -= 180
    return c, (w, h), angle
def is_close(rect1, rect2, angle_tol, height_tol, width_tol, cy_tol):
    """检查两个旋转矩形是否足够接近。"""
    (cx1, cy1), (w1, h1), angle1 = rect1
    (cx2, cy2), (w2, h2), angle2 = rect2
    return (min(abs(angle1 - angle2), 360 - abs(angle1 - angle2)) <= angle_tol and
            abs(h1 - h2) <= height_tol and
            abs(w1 - w2) <= width_tol and
            abs(cy1 - cy2) <= cy_tol)
def put_text(img, color, rect):
    center_x, center_y = map(int, rect[0])
    cv2.putText(img, f"({center_x}, {center_y})", (center_x, center_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
def do_polygons_intersect(a, b):
    """使用分离轴定理检查两个多边形是否相交。"""
    for polygon in (a, b):
        for i in range(len(polygon)):
            p1, p2 = polygon[i], polygon[(i + 1) % len(polygon)]
            normal = (p2[1] - p1[1], p1[0] - p2[0])
            min_a, max_a = project_polygon(a, normal)
            min_b, max_b = project_polygon(b, normal)
            if max_a < min_b or max_b < min_a:
                return False
    return True
def project_polygon(polygon, axis):
    """将多边形投影到给定的轴上。"""
    projections = [np.dot(point, axis) for point in polygon]
    return min(projections), max(projections)
def img_processed(img, val, gamma):
    resized_img = cv2.resize(img, (640, 480))
    img_float = img_as_float(resized_img)
    img_float = (exposure.adjust_gamma(img_float, gamma) * 255).astype(np.uint8)
    img_gray = cv2.cvtColor(img_float, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(img_gray, val, 255, cv2.THRESH_BINARY)
    return binary_image, resized_img, img_float
def find_light(color, img_binary,img):
    contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rotated_rects = [adjust_rotated_rect(cv2.minAreaRect(contour)) 
                     for contour in contours if cv2.contourArea(contour) > 100]
    
    filtered_rotated_rects = []
    for i, rect_a in enumerate(rotated_rects):
        box_a = cv2.boxPoints(rect_a).astype(int)
        if not any(do_polygons_intersect(box_a, cv2.boxPoints(rotated_rects[j]).astype(int)) 
                   for j in range(len(rotated_rects)) if i != j):
            filtered_rotated_rects.append(rect_a)
    
    for rect in filtered_rotated_rects:
        box = cv2.boxPoints(rect).astype(int)
        cv2.drawContours(img, [box], 0, color, 3) 
    return filtered_rotated_rects
def armortype(img_raw, rotated_rect):
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

    except Exception :
        print("no armor")
        return -1
def track_armor(img, img_raw, rotated_rects, angle_tol=25, height_tol=100, width_tol=100, cy_tol=100):
    rects_copy = rotated_rects[:]
    all_groups = []
    
    while rects_copy:
        rect1 = rects_copy.pop(0)
        group = [rect1]
        
        for i in range(len(rects_copy) - 1, -1, -1):
            if is_close(rect1, rects_copy[i], angle_tol, height_tol, width_tol, cy_tol):
                group.append(rects_copy.pop(i))

        all_groups.append(group)
    
    armor_rects = []
    for rect_group in all_groups:
        if not rect_group:
            continue
        
        points = np.concatenate([cv2.boxPoints(rect) for rect in rect_group])
        merged_rect = cv2.minAreaRect(points)
        if merged_rect[1][0] * merged_rect[1][1] >= 2000:
            if 0 <= merged_rect[1][0] / merged_rect[1][1] <= 4:
                armor_rects.append(adjust_rotated_rect(merged_rect))
    
    armors_dict = {}
    for armor_rect in armor_rects:
        center, (width, height), angle = armor_rect
        box = cv2.boxPoints(((center[0], center[1]), (width, height), angle)).astype(int)
        color_result = armortype(img_raw, armor_rect)
        class_id = 1 if color_result == 1 else 7 if color_result == 0 else None
        if class_id is not None:
            armors_dict[f"{center[0]}"] = {"class_id": class_id, "height": height, "center": [center[0], center[1]]}
            color = (255, 0, 0) if color_result == 1 else (0, 0, 255)
            cv2.drawContours(img, [box], 0, color, 3)
            put_text(img, color, armor_rect)
    return armors_dict
def detect_armor(img, val=23, gamma=20, color=(0,0,0)):
    img_binary, resized_img, img_blur = img_processed(img, val, gamma)
    rotated_rects = find_light(color, img_binary,resized_img)
    armors_dict = track_armor(resized_img, img_blur, rotated_rects)
    print(armors_dict)
    cv2.imshow("armor", resized_img)
def destroy():
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    img = cv2.imread('detector/combine.png')
    detect_armor(img)
    destroy()

