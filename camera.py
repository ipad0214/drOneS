# -*- coding: utf-8 -*-

import cv2
import numpy as np
 
 
class VideoCamera(object):
    def __init__(self, onArm=True): 
        if onArm:
            self.video = cv2.VideoCapture('resources/test.mp4')
            print("streaming test video")
        else:
            self.video = cv2.VideoCapture(0)
            print("streaming live video")

    def __del__(self):
        self.video.release()
        
    def get_frame(self):
        success, image = self.video.read()
        
        ret, jpeg = cv2.imencode('.jpg', image)
        
        return jpeg.tobytes()