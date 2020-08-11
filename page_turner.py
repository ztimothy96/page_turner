import keyboard
import os
import shlex
import time
import cv2
import imutils
from imutils.video import VideoStream
from detector import WinkDetector


FOLDER = "/Users/timothyzhou/Desktop/piano rep/"
FILE = "brahms 1.pdf"
START_PAGE = 3
MIN_WINK_TIME = 0.5 # number of seconds a wink should last before turning page
COOLDOWN_TIME = 2 # number of seconds between consecutive detected winks

def set_up_score(folder, file, start_page):
    path = folder + file
    os.system("open " + shlex.quote(path))

    time.sleep(3) # wait for open process to complete
    keyboard.send("command + L") # full screen in Acrobat
    for _ in range(START_PAGE-1):
        keyboard.send("right")
    return

def turn_pages():
    detector = WinkDetector()
    vs = VideoStream(src=0).start()
    winking_left = False #whether the face was previously winking
    winking_right = False
    left_wink_start = -1
    right_wink_start = -1

    while True:
        t = time.time()
        frame = vs.read()
        wink_type = detector.get_wink_type(frame)
        
        if winking_left:
            if t - left_wink_start > MIN_WINK_TIME:
                keyboard.send("left")
                winking_left = False
                time.sleep(COOLDOWN_TIME)
            elif wink_type != "left":
                winking_left = False

        elif winking_right:
            if t - right_wink_start > MIN_WINK_TIME:
                keyboard.send("right")
                winking_right = False
                time.sleep(COOLDOWN_TIME)
            elif wink_type != "right":
                winking_right = False

        elif wink_type == "left":
            winking_left = True
            left_wink_start = t

        elif wink_type == "right":
            winking_right = True
            right_wink_start = t
            
        if cv2.waitKey(1) = 27:
            break # esc to quit

    vs.stop()
    cv2.destroyAllWindows()

set_up_score(FOLDER, FILE, START_PAGE)
turn_pages()
