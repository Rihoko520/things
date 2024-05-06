#### 在python代码中实现文件移动

import shutil
import os

# 获取当前工作目录
current_dir = os.getcwd()

# 指定要移动的文件名
file_to_move = 'square.jpg'

# 指定目标目录
destination_dir = 'D:\\Kaoru\\files\\Study\\python\\git\\week - 9\\out\\1'
# 此处路径只能用绝对路径，可以通过查看报错内容来查找你要的绝对路径位置，也可以直接复制目标目录的绝对路径过来，注意一定要双杠“\\”

# 构建文件的完整路径
source_path = os.path.join(current_dir, file_to_move)
destination_path = os.path.join(destination_dir, file_to_move)

# 使用shutil.move()函数移动文件
shutil.move(source_path, destination_path)


# cv2写法
### 有局限性，一般只可以写入到当前目录里面的文件夹

import cv2
image_path = '1.jpg'

image = cv2.imread(image_path)
##########################################################################################
                                                                           #This
#保存测试图片到相应区域（只能是当前目录或者当前目录下面的文件夹                #Is                                    
#（文件夹/文件名）                                                          #A
save_path = 'finish/1/color.jpg'                                          #Saving
cv2.imwrite(save_path, image)                                             #Spot!
                                                                           #
##########################################################################################