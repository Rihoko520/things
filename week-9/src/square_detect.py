import cv2
import numpy as np

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

def resize(img):
    target_width = 640
    target_height = 480

    # 调整图像大小
    img = cv2.resize(img, (target_width, target_height))
    return img

def square(image_path):
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    blur = cv2.GaussianBlur(gray, (9, 9), 0)  # 高斯滤波去噪
    enhanced_ = enhanced_image(blur)
    final_ = contours_detecto(enhanced_,img)
    return final_

if __name__ == "__main__":
    #获取图片位置
    project = '1'
    
    image_path = f'{project}.jpg'
    final_ = square(image_path)
    
    # 显示检测出来的轮廓
    cv2.namedWindow("square", cv2.WINDOW_NORMAL)
    cv2.imshow("square", final_)

    cv2.waitKey(0)
    cv2.destroyAllWindows()