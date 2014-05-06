
import freenect
import blob
import cv2


class DepthClassifier(object):

    def __init__(self, depth_thresh, **kwargs):
        self.depth_thresh = depth_thresh
        self.min_blob_size = kwargs.get("min_blob_size", 0)
        self.max_blob_size = kwargs.get("max_blob_size", None)

    def __call__(self, video, depth):
        _, depth_bw = cv2.threshold(
            depth, self.depth_thresh, 255, cv2.THRESH_BINARY_INV
        )

        blobs = blob.get_blobs(
            depth_bw, self.min_blob_size, self.max_blob_size
        )

        centroid_list = list()

        for b in blobs:
            centroid = b.get_centroid()
            centroid.set_z(depth[centroid.y, centroid.x])

            centroid_list.append(centroid)

        return centroid_list


