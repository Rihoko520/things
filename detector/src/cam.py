import cv2
from detector import find_armor

url='http://192.168.3.195:4747/video/'
video_stream = cv2.VideoCapture("1.mp4")
while True:  
    ret,frame = video_stream.read()
    # 检查图像是否成功读取
    if not ret:
        print("Error: Failed to read frame")
        break
    save_path='frame.jpg'
    cv2.imwrite(save_path,frame)
    # 读取图像
    img = cv2.imread('frame.jpg')
    find_armor(frame)
    print(f"fps={ret}")
    # 等待按键，如果按下'q'则退出循环  
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break  
video_stream.release()
cv2.destroyAllWindows()