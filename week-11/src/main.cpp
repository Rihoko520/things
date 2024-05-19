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

Mat denoise(const Mat& image) {
    Mat denoised_image;
    fastNlMeansDenoisingColored(image, denoised_image, 10, 10, 7, 21);
    return denoised_image;
}

Mat enhanceImage(const Mat& denoised_image) {
    Mat enhanced_image;
    double alpha = 1.5; // 对比度增强参数
    int beta = 15; // 亮度增强参数
    convertScaleAbs(denoised_image, enhanced_image, alpha, beta);
    return enhanced_image;
}

Mat detectContours(const Mat& enhanced_image) {
    Mat edges;
    Canny(enhanced_image, edges, 50, 150);

    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
    findContours(edges, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);

    Mat marked_image = enhanced_image.clone();

    for (size_t i = 0; i < contours.size(); i++) {
        double area = contourArea(contours[i]);
        if (area > 2000) {
            vector<Point> approx;
            double perimeter = arcLength(contours[i], true);
            approxPolyDP(contours[i], approx, 0.02 * perimeter, true);

            if (approx.size() == 4) {
                // 计算中心点
                Moments mu = moments(contours[i]);
                Point center(mu.m10 / mu.m00, mu.m01 / mu.m00);

            // 绘制中心点
                circle(marked_image, center, 5, Scalar(0, 255, 0), -1);
                putText(marked_image, std::to_string(center.x) + ", " + std::to_string(center.y), center, FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);

            // 绘制顶点并标记坐标
                for (int j = 0; j < 4; j++) {
                    circle(marked_image, approx[j], 5, Scalar(255, 0, 0), -1);
                    putText(marked_image, std::to_string(approx[j].x) + ", " + std::to_string(approx[j].y), approx[j], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(255, 0, 0), 2);
                    }
                // 绘制轮廓
                drawContours(marked_image, contours, static_cast<int>(i), Scalar(0, 0, 255), 2);
            }
        }
    }

    return marked_image;
}

int main() {
    Mat image = detectContours("image.jpg");
    Mat denoised_image = denoise(image);
    Mat enhanced_image = enhanceImage(denoised_image);
    Mat final_image = detectContours(enhanced_image);
    Mat Final_image;
    cv::addWeighted(image, 0.6, final_image, 0.6, 0, Final_image);    
    namedWindow("final", WINDOW_NORMAL);
    imshow("final", Final_image);
    waitKey(0);
    destroyAllWindows();
    
    return 0;
}