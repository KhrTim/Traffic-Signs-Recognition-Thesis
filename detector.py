import torch
import numpy as np
import cv2
from time import time
from model_controller import ModelController
from PIL import Image

class ObjectDetector:
    def __init__(self, model_controller: ModelController):
        self.model = model_controller.get_model()
        self.classes = model_controller.get_classes()

    def get_labeled_image(self, cv2_frame):
        self.frame = cv2_frame
        results = self.score_frame(self.frame)
        labeled_image = self.plot_boxes(results, self.frame)
        labeled_image = cv2.cvtColor(labeled_image,cv2.COLOR_BGR2RGB)
        labeled_image = Image.fromarray(labeled_image)
        return labeled_image

    def score_frame(self, frame):
        frame = [frame]
        results = self.model(frame)
        print(results)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord


    def class_to_label(self, x):
        return self.classes[int(x)]


    def plot_boxes(self, results, frame):
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.3:
                x1, y1, x2, y2 = int(
                    row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(
                    labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame