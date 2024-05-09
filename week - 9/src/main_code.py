import cv2
import numpy as np
import shutil
import os

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
    image = cv2.imread(image_path)
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


def safe_1(marked_image,name):                                            
    #保存测试图片到当前目录                                                  
    #（文件夹/文件名）                                                         
    save_path = f'{name}.jpg'                                          
    cv2.imwrite(save_path, marked_image)                                      



def safe_2(name,project):
    # 获取当前工作目录
    current_dir = os.getcwd()

    # 指定要移动的文件名
    # 使用 f-string 格式化文件名
    file_to_move = f'{name}.jpg'

    # 指定目标目录
    destination_dir = f'D:\\Kaoru\\files\\Study\\python\\git\\week - 9\\out\\{project}'
    # 此处路径只能用绝对路径，可以通过查看报错内容来查找你要的绝对路径位置，也可以直接复制目标目录的绝对路径过来，注意一定要双杠“\\”

    # 构建文件的完整路径
    source_path = os.path.join(current_dir, file_to_move)
    destination_path = os.path.join(destination_dir, file_to_move)

    # 使用shutil.move()函数移动文件
    shutil.move(source_path, destination_path)



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

if __name__ == "__main__":
    #获取图片位置
    #原图片名字(可通过直接该project的名字来选定图片直接进行处理)
    project = '5'
    
    image_path = f'{project}.jpg'
    denoised_ = denoise(image_path)
    enhanced_ = enhanced_image(denoised_)
    final_ = contours_detecto(enhanced_)
    #处理后的图像文件名
    name ='square'
    safe_1(final_,name)
    safe_2(name,project)


    image = detectto(image_path)
    #原图像文件名
    name ='color'
    safe_1(image,name)
    safe_2(name,project)

    #合并图像
    name ='combined'
    Final_image = cv2.addWeighted(image, 0.6, final_, 0.6, 0)
    safe_1(Final_image,name)
    safe_2(name,project)
    # 显示合并图像
    cv2.namedWindow('combined', cv2.WINDOW_NORMAL)
    cv2.imshow('combined', Final_image)    
    # 显示带有红色点和绿色点的图像
    cv2.namedWindow('color', cv2.WINDOW_NORMAL)
    cv2.imshow('color', image)
    # 显示检测出来的轮廓
    cv2.namedWindow("square", cv2.WINDOW_NORMAL)
    cv2.imshow("square", final_)

    cv2.waitKey(0)
    cv2.destroyAllWindows()