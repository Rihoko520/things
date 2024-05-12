## Cmake的对于cv的使用(for linux)
### 原理
- **cmake**相当于一个软件，他会把你写的代码打包整合成一个大的程序，每次运行只需要点开那个集合的程序就可以运行自己的代码
### 使用方法
#### 构建一个cmakelist.txt
- [cmakelist](src/CMakeLists.txt)
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

#### 构建cmake程序打包仓库

- 新建一个Bulid文件夹
- 在该文件夹打开终端
    - 导入cmake数据
        ```bash
        cmake .
        ```

#### 构建完成Bulid后，现在就可以开始包装自己的主函数了
- 将调好的  cmakelist.txt  和主函数一起放进build文件夹
- 在终端输入make开始打包
    ```bash
    make
    ```
#### 打包完成后就可以直接点击打包好的程序来运行了
（有个齿轮那个）
- 也可以直接点开那个工程(齿轮那个文件)
