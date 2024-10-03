import cv2
from skimage import exposure

# 全局变量，用于存储当前的 gamma 和阈值
gamma = 0.7
threshold_value = 128

# 滑动条的回调函数，用于更新阈值
def update_threshold(val):
    global threshold_value
    threshold_value = val
    apply_changes()  # 应用更改

# 滑动条的回调函数，用于更新 gamma 值
def update_gamma(val):
    global gamma
    gamma = val / 100.0  # 将 gamma 值从 (0-100) 缩放到 (0.0-1.0)
    apply_changes()  # 应用更改

# 应用更改的函数
def apply_changes():
    # 应用 gamma 校正
    gamma_corrected = exposure.adjust_gamma(image, gamma)
    # 转换为灰度图像
    gray_image = cv2.cvtColor(gamma_corrected, cv2.COLOR_BGR2GRAY)
    # 应用二值化处理
    _, binary_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
    # 显示二值化后的图像
    cv2.imshow('Binary Image', binary_image)

# 加载图像
image = cv2.imread('detector/1.png')

if image is None:
    print("Error: Could not read the image.")
else:
    print("Image loaded successfully.")
    image = cv2.resize(image, (640, 480))  # 将图像调整为 640x480

    # 创建一个窗口来显示二值化图像
    cv2.namedWindow('Binary Image')

    # 创建一个滑动条，用于调整阈值
    cv2.createTrackbar('Threshold', 'Binary Image', 0, 255, update_threshold)
    cv2.setTrackbarPos('Threshold', 'Binary Image', threshold_value)  # 设置初始位置

    # 创建一个滑动条，用于调整 gamma 值
    cv2.createTrackbar('Gamma', 'Binary Image', int(gamma * 100), 2000, update_gamma)  # 缩放到 0-300
    cv2.setTrackbarPos('Gamma', 'Binary Image', int(gamma * 100))  # 设置初始位置

    # 初始显示二值化图像
    apply_changes()

    # 等待用户按键
    cv2.waitKey(0)
    cv2.destroyAllWindows()