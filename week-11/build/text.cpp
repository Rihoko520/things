#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

int main() {
  // VideoCapture cap("http://192.168.1.209:4747/video");
  VideoCapture cap(0);

  if (!cap.isOpened()) {
    cout << "Error opening video stream or file" << endl;
    return -1;
  }

  Mat frame;
  namedWindow("Video", WINDOW_NORMAL);

  while (true) {
    cap >> frame;

    if (frame.empty()) {
      cout << "End of video stream" << endl;
      break;
    }

    imshow("Video", frame);

    if (waitKey(1) == 27) {  // Press ESC to exit
      break;
    }
  }

  cap.release();
  destroyAllWindows();

  return 0;
}