#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

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
    Mat image = imread("image.jpg");
    Mat denoised_image = denoise(image);
    Mat enhanced_image = enhanceImage(denoised_image);
    Mat final_image = detectContours(enhanced_image);
    imshow("Contours Detection", final_image);
    waitKey(0);
    destroyAllWindows();
    return 0;
}