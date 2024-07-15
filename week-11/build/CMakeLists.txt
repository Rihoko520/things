cmake_minimum_required(VERSION 2.8)
project( DisplayImage )
# OpenCV 的 CMake 配置文件目录
set(OpenCV_DIR "/usr/local/include/opencv4")
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( text text.cpp )
target_link_libraries( text ${OpenCV_LIBS} )
