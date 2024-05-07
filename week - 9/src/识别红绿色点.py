import cv2
import numpy as np

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
    project = '1'
    
    image_path = f'{project}.jpg'
    image = detectto(image_path)
# 显示带有红色点和绿色点的图像
    cv2.namedWindow('color', cv2.WINDOW_NORMAL)
    cv2.imshow('color', image)


    cv2.waitKey(0)
    cv2.destroyAllWindows()