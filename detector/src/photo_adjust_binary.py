import cv2
from skimage import exposure
# 滑动条的回调函数
def update_threshold(val):
    # 从滑动条获取当前的阈值
    threshold_value = val
    # 应用二值化处理
    _, binary_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
    # 显示二值化后的图像
    cv2.imshow('Binary Image', binary_image)

# 加载图像
image = cv2.imread('detector/3.png')
gamma_corrected = exposure.adjust_gamma(image, gamma=0.7) #Example: Darkens the image
blur = cv2.GaussianBlur(gamma_corrected, (11, 11), 0)  # 高斯滤波去噪
# 转换为灰度图像
gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

# 创建一个窗口
cv2.namedWindow('Binary Image')

# 创建一个滑动条，用于调整阈值
cv2.createTrackbar('Threshold', 'Binary Image', 0, 255, update_threshold)

# 初始化阈值
cv2.setTrackbarPos('Threshold', 'Binary Image', 128)  # 设置滑动条的初始位置为128

# 初始显示二值化图像
update_threshold(128)

# 等待用户按键
cv2.waitKey(0)
cv2.destroyAllWindows()