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
