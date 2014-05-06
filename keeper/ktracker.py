
import freenect
import numpy as np


class KinectTracker(object):

    def __init__(self, classifier, drawer=None):
        self.classifier = classifier
        self.drawer = drawer

    def track(self):
        video = freenect.sync_get_video()[0]
        depth = freenect.sync_get_depth()[0]
        depth = depth.astype(np.float32)

        tr_points = self.classifier(video, depth)

        if self.drawer:
            self.drawer(video, depth, tr_points)

        return tr_points

