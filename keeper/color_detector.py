#!/usr/bin/env python2.7
import sys

import cv2
import freenect
import numpy as np


class ColorDetector(object):
    def __init__(self, **kwargs):
        CV_CAP_PROP_FRAME_WIDTH = 3
        CV_CAP_PROP_FRAME_HEIGHT = 4

        # video frame dimensions
        width = kwargs.get("video_width", 640)
        height = kwargs.get("video_height", 480)

        # initial HSV values
        hsv_vals = (
            20,  # hue_min
            0,  # sat_min
            0,  # val_min
            75,  # hue_max
            255,  # sat_max
            255,  # val_max
        )

        # find and initialize the webcam
        self.capture = cv2.VideoCapture(0)
        self.capture.set(CV_CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(CV_CAP_PROP_FRAME_HEIGHT, height)

        # create gui
        self.create_hsv_gui(hsv_vals)

        # detector states
        self.detection_area = False
        self.get_hsv = False

    def hsv_callback(self, val):
        pass

    def create_hsv_gui(self, hsv_vals):
        win = "hsv"
        cv2.namedWindow(win)

        # HUE
        cv2.createTrackbar("Hue Min", win, hsv_vals[0], 255, self.hsv_callback)
        cv2.createTrackbar("Hue Max", win, hsv_vals[3], 255, self.hsv_callback)

        # SAT
        cv2.createTrackbar("Sat Min", win, hsv_vals[1], 255, self.hsv_callback)
        cv2.createTrackbar("Sat Max", win, hsv_vals[4], 255, self.hsv_callback)

        # VAL
        cv2.createTrackbar("Val Min", win, hsv_vals[2], 255, self.hsv_callback)
        cv2.createTrackbar("Val Max", win, hsv_vals[5], 255, self.hsv_callback)

    def draw_detection_area(self, video_frame):
        # get video frame center
        center_x = video_frame.shape[1] / 2
        center_y = video_frame.shape[0] / 2

        # draw a small red rectange in the middle
        area_size = 10
        top_left = (center_x - area_size, center_y - area_size)
        bottom_right = (center_x + area_size, center_y + area_size)
        cv2.rectangle(video_frame, top_left, bottom_right, (0, 0, 255), 3)

        return video_frame

    def pixel_get_hsv(self, video_frame):
        # get video frame center
        center_x = video_frame.shape[1] / 2
        center_y = video_frame.shape[0] / 2

        # get hsv pixel value from the center of the video frame
        hsv_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2HSV)
        hsv = hsv_frame[center_y][center_x]
        hue = hsv[0]
        sat = hsv[1]
        val = hsv[2]
        print "PIXEL HSV:", hue, sat, val

        return (hue, sat, val)

    def get_hsv_values(self):
        # get hsv values from hsv gui
        lbound = (
            cv2.getTrackbarPos("Hue Min", "hsv"),
            cv2.getTrackbarPos("Sat Min", "hsv"),
            cv2.getTrackbarPos("Val Min", "hsv")
        )

        ubound = (
            cv2.getTrackbarPos("Hue Max", "hsv"),
            cv2.getTrackbarPos("Sat Max", "hsv"),
            cv2.getTrackbarPos("Val Max", "hsv")
        )

        return (lbound, ubound)

    def update_hsv_gui(self, hsv, hue_range=10):
        hue, sat, val = hsv

        hue_min = hue - hue_range if hue - hue_range > 0 else 0
        hue_max = hue + hue_range if hue + hue_range < 255 else 255
        sat_min = sat
        sat_max = 255
        val_min = val
        val_max = 255

        cv2.setTrackbarPos("Hue Min", "hsv", hue_min)
        cv2.setTrackbarPos("Hue Max", "hsv", hue_max)

        cv2.setTrackbarPos("Sat Min", "hsv", sat_min)
        cv2.setTrackbarPos("Sat Max", "hsv", sat_max)

        cv2.setTrackbarPos("Val Min", "hsv", val_min)
        cv2.setTrackbarPos("Val Max", "hsv", val_max)

    def detect_color(self, orig_frame, thres_frame, contour_area=300):
        kernel = np.ones((5, 5), np.uint8)
        dilate = cv2.dilate(thres_frame, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(
            dilate,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # loop through discovered contour
        detected = []
        for i in range(len(contours)):
            if cv2.contourArea(contours[i]) > contour_area:
                # obtain contour center and append to detected
                M = cv2.moments(contours[i])
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                detected.append((cx, cy))

                # draw detected contour
                cv2.drawContours(orig_frame, contours, i, (0, 255, 0), 3)

                # draw center in detected contour
                top_left = (cx, cy)
                bottom_right = (cx + 5, cy + 5)
                color = (255, 0, 0)  # blue
                cv2.rectangle(orig_frame, top_left, bottom_right, color, 3)

                # draw rectangle around detected contour
                x, y, w, h = cv2.boundingRect(contours[i])
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                color = (0, 0, 255)  # red
                cv2.rectangle(orig_frame, top_left, bottom_right, color, 2)

        cv2.imshow("Detected", orig_frame)

        return detected

    def display(self, frame):
        # draw detection area
        if self.detection_area:
            self.draw_detection_area(frame)

        # detect hsv value in detection area and update hsv gui
        if self.get_hsv:
            hsv = self.pixel_get_hsv(frame)
            self.update_hsv_gui(hsv)

        # draw video and threshold windows
        lbound, ubound = self.get_hsv_values()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        thres_frame = cv2.inRange(hsv_frame, lbound, ubound)

        cv2.imshow('Threshold', thres_frame)

        # detect color objects
        del detected_objects[:]
        objects = self.detect_color(frame, thres_frame)
        detected_objects.extend(objects)

    def events(self, video_frame, cleanup_func=None):
        # keyboard events
        key = cv2.waitKey(50)

        if key == 27 or key == ord('q'):
            if cleanup_func is None:
                sys.exit(0)
            else:
                cleanup_func()

        elif key == ord('d'):
            self.detection_area = not self.detection_area

        elif key == ord('h'):
            self.get_hsv = not self.get_hsv

        else:
            self.display(video_frame)

    def cleanup(self):
        self.capture.release()
        cv2.destroyAllWindows()

    def init_webcam(self, detected_objects):
        while (self.capture.isOpened()):
            ret, frame = self.capture.read()
            self.events(frame, self.cleanup())

    def init_kinect(self, detected_object):
        while True:
            img = freenect.sync_get_video()[0]
            frame = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            self.events(frame)


if __name__ == "__main__":
    detected_objects = []
    detector = ColorDetector()
    detector.init_kinect(detected_objects)

    print "Detected objects:", detected_objects
