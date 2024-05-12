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
                drawContours(marked_image, contours, static_cast<int>(i), Scalar(200, 250, 10), 2);
            }
        }
    }

    return marked_image;
}

int main() {
    string project = "1";
    string image_path = project + ".jpg";
    Mat image = imread(image_path);

    Mat denoised_image = denoise(image);
    Mat enhanced_image = enhanceImage(denoised_image);
    Mat final_image = detectContours(enhanced_image);

    imshow("Contours Detection", final_image);
    waitKey(0);
    destroyAllWindows();

    return 0;
}