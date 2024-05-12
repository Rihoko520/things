## Cmake的对于cv的使用
### 原理
- **cmake**相当于一个软件，他会把你写的代码打包整合成一个大的程序，每次运行只需要点开那个集合的程序就可以运行自己的代码
### 使用方法
#### 构建一个cmakelist.txt
- 文件内容如下

    ```bash
    cmake_minimum_required(VERSION 2.8)
    project( DisplayImage )
    find_package( OpenCV REQUIRED )
    include_directories( ${OpenCV_INCLUDE_DIRS} )
    add_executable( DisplayImage DisplayImage.cpp )
    target_link_libraries( DisplayImage ${OpenCV_LIBS} )
    ```

#### 写自己的cv主函数
- 范例
    ```c++
    #include <opencv2/highgui.hpp>
    #include <iostream>
    int main( int argc, char** argv )
    {
        cv::Mat image;
        image = cv::imread("Lena.jpg",cv::IMREAD_COLOR);
        if(! image.data)
            {
                std::cout<<"Could not open file" << std::endl;
                return -1;
            }
        cv::namedWindow("namba image", cv::WINDOW_AUTOSIZE);
        cv::imshow("namba image", image);
        cv::waitKey(0);
        return 0;
    }
  ```
- 保存为*name.cpp*文件（name是任意名字）

#### 构建cmake程序集合仓库（即存放你程序的文件夹）
**文件夹要包含你的主函数和cmakelist文件
- 在该文件夹打开终端
    - 构建工程
        ```bash
        cmake .
        make
        ```

#### 构建完成，现在就可以开始运行自己的代码了
- 在文件夹打开终端输入运行的文件名字（名字为自己创建的main程序名字，cpp那个）
    
    ```bash
    ./name
    ```
