#### 在python代码中实现文件移动

import shutil
import os
import cv2
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