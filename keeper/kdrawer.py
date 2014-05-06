
import cv2

class KinectDrawer(object):

    def __init__(self):
        pass

    def __call__(self, video, depth, tr_points):
        video = cv2.cvtColor(video, cv2.COLOR_RGB2BGR)
        for tr_point in tr_points:
            cv2.circle(
                video, (tr_point.x, tr_point.y), 10, (0, 0, 255), 2
            )
        cv2.imshow("Kinect Video", video)
        cv2.waitKey(1)

