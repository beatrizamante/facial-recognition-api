import cv2
import numpy as np


class CameraModel:
    def __init__(self,  camera_width=0, camera_height=0, tolerance = 150):
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.center_X = self.camera_width / 2
        self.center_y = self.camera_height / 2
        self.face_x = None
        self.face_y = None
        self.tolerance = tolerance
        
    def update_dimensions(self, width, height):
        self.camera_width = width
        self.camera_height = height
        self.center_X = width / 2
        self.center_y = height / 2
        
    def find_center_face(self, face_locations):
        for face_location in face_locations:
            top, right, bottom, left = face_location
            self.face_x = (right + left) / 2
            self.face_y = (top + bottom) / 2
        
    def check_if_centered(self):
        if self.face_x is not None and self.face_y is not None:
            if abs(self.face_x - self.center_X) < self.tolerance and abs(self.face_y - self.center_y) < self.tolerance:
                return True
        return False
    
