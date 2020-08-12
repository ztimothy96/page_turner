import cv2
import imutils
import dlib
import numpy as np
from imutils import face_utils

'''
A simple HOG-based face detector
Head tilt detection is based on the ratio between eye lengths
'''

PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat" # path to facial landmarks detector
THRESH = 0.80 #todo: maybe add a calibration step for convenience

def dist(p1, p2):
    return ((p2[0]-p1[0])**2 + (p2[1]-p1[1])*2)**0.5

def ratio(eye):
    return (dist(eye[1], eye[5]) + dist(eye[2], eye[4])) / (2.0 * dist(eye[0], eye[3]))

class TurnDetector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(PREDICTOR_PATH)
        self.thresh = THRESH
        self.lstart, self.lend = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
        self.rstart, self.rend = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
        
    def get_turn_type(self, frame, display=False):
        frame = imutils.resize(frame, width=400)
        found, face, keypoints = self.detect_keypoints(frame)
        left_eye, right_eye, turn_type = self.classify_turn(found, keypoints)
        if display:
            self.visualize(frame, found, face, left_eye, right_eye)
        return turn_type

    def detect_keypoints(self, frame):
        found = False # whether a face is found
        face = None
        keypoints = None
        get_size = lambda face: (face.right()-face.left())*(face.top()-face.bottom())
        faces = self.detector(frame, 1)
        
        if len(faces) > 0:
            found = True
            face = max(faces, key=get_size) # largest face is probably the performer
            keypoints = self.predictor(frame, face)
            keypoints = face_utils.shape_to_np(keypoints)
        return found, face, keypoints
    
    def classify_turn(self, found, keypoints):
        if found == False:
            return None, None, None
        left_eye = keypoints[self.lstart:self.lend]
        right_eye = keypoints[self.rstart:self.rend]
        left_eye_ratio = ratio(left_eye)
        right_eye_ratio = ratio(right_eye)
        
        if right_eye_ratio < self.thresh * left_eye_ratio:
            return left_eye, right_eye, "left"
        if left_eye_ratio < self.thresh * right_eye_ratio:
            return left_eye, right_eye, "right"
        return None, None, None

    def visualize(self, frame, success, face, left_eye, right_eye):
        if success:
            cv2.rectangle(frame, (face.left(), face.bottom()), (face.right(), face.top()),
			(0, 0, 255), 2)
        cv2.imshow("Frame", frame)
