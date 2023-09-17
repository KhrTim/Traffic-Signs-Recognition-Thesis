import torch
import numpy as np
import cv2
from time import time
from source_mode import SourceMode


class SourceController:
    def __init__(self, source_mode: SourceMode,source_path=None):
        self.source_path = source_path
        self.source_mode = source_mode
        if self.source_mode == SourceMode.VIDEO:
            assert self.source_path
            self.cap = cv2.VideoCapture(self.source_path)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        elif self.source_mode == SourceMode.CAMERA:
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = None

    def return_latest_frame(self):
        self.retrieve_frame()
        return self.frame

    def current_mode(self) -> SourceMode:
        return self.source_mode

    def current_filename(self):
        return self.source_path

    def retrieve_frame(self):
        if self.source_mode == SourceMode.IMAGE:
            assert self.source_path
            self.frame = cv2.imread(self.source_path)
        elif self.source_mode == SourceMode.VIDEO:
            assert self.source_path
            assert self.cap.isOpened()
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    # frame = cv2.resize(frame, (640, 640))
                    self.frame = frame
                else:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = self.cap.read()
                    # frame = cv2.resize(frame, (640, 640))
                    self.frame = frame

        elif self.source_mode == SourceMode.CAMERA:
            assert self.cap.isOpened()

            if self.cap.isOpened():
                ret, frame = self.cap.read()
                assert ret

                # frame = cv2.resize(frame, (640, 640))
                self.frame = frame


    def clear(self):
        if self.cap:
            self.cap.release()
            self.cap = None