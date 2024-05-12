#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
using namespace cv;

Mat detectContours(string image_path) {
    Mat image = imread(image_path);
    
    Mat hsv;
    cvtColor(image, hsv, COLOR_BGR2HSV);
    
    Scalar lower_red = Scalar(152, 127, 25);
    Scalar upper_red = Scalar(179, 193, 255);  
    Scalar lower_green = Scalar(48, 82, 39);  
    Scalar upper_green = Scalar(121, 247, 255); 
    
    Mat mask_red, mask_green;
    inRange(hsv, lower_red, upper_red, mask_red);
    inRange(hsv, lower_green, upper_green, mask_green);
    
    vector<vector<Point>> contours_red, contours_green;
    findContours(mask_red, contours_red, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
    findContours(mask_green, contours_green, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
    
    for (auto contour : contours_red) {
        Rect rect = boundingRect(contour);
        rectangle(image, rect, Scalar(0, 0, 255), 2);
        putText(image, "Red", Point(rect.x + rect.width / 2, rect.y + rect.height / 2), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 0, 255), 2);
    }
    
    for (auto contour : contours_green) {
        Rect rect = boundingRect(contour);
        rectangle(image, rect, Scalar(0, 255, 0), 2);
        putText(image, "Green", Point(rect.x + rect.width / 2, rect.y + rect.height / 2), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 255, 0), 2);
    }
    
    return image;
}

int main() {
    Mat image = detectContours("image.jpg");
    
    namedWindow("color", WINDOW_NORMAL);
    imshow("color", image);
    
    waitKey(0);
    destroyAllWindows();
    
    return 0;
}