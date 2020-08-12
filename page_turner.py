import imutils
import numpy as np
import time
import cv2
import keyboard
import os
import shlex
from detector import TurnDetector


FOLDER = "/Users/timothyzhou/Desktop/piano rep/"
FILE = "book2/wtc book 2 peters.pdf"
START_PAGE = 3
MIN_TURN_TIME = 0.3 # number of seconds head tilt should last before turning page
COOLDOWN_TIME= 2 # number of seconds between consecutive detected turns

'''
this function will open the score and flip to the desired first page
only for those who are truly lazy
'''

def set_up_score(folder, file, start_page):
    path = folder + file
    os.system("open " + shlex.quote(path))

    time.sleep(3) # wait for open process to complete
    keyboard.send("command + L") # full screen in Acrobat
    for _ in range(START_PAGE-1):
        keyboard.send("right")
    return

'''
the main page-turning function!
after calling, make sure the pdf window is active
turn your head slightly for a second in the direction you wish the page to turn
voila! enjoy :)
'''

def turn_pages():
    detector = TurnDetector()
    camera = cv2.VideoCapture(0)
    turning_left = False # whether the face was previously turning
    turning_right = False
    left_turn_start = -1
    right_turn_start = -1

    while True:
        t = time.time()
        _, frame = camera.read()
        turn_type = detector.get_turn_type(frame)
        
        if turning_left:
            if t - left_turn_start > MIN_TURN_TIME:
                keyboard.send("left")
                turning_left = False
                time.sleep(COOLDOWN_TIME)
            elif turn_type != "left":
                turning_left = False

        elif turning_right:
            if t - right_turn_start > MIN_TURN_TIME:
                keyboard.send("right")
                turning_right = False
                time.sleep(COOLDOWN_TIME)
            elif turn_type != "right":
                turning_right = False

        elif turn_type == "left":
            turning_left = True
            left_turn_start = t

        elif turn_type == "right":
            turning_right = True
            right_turn_start = t
            
        if cv2.waitKey(1) == 27:
            break # esc to quit

    camera.release()
    cv2.destroyAllWindows()


set_up_score(FOLDER, FILE, START_PAGE)
turn_pages()

