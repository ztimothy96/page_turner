import keyboard
import os
import shlex
import time

FOLDER = "/Users/timothyzhou/Desktop/piano rep/"
FILE = "brahms 1.pdf"
START_PAGE = 3

def set_up_score(folder, file, start_page)
    path = folder + file
    os.system("open " + shlex.quote(path))

    time.sleep(3) # wait for open process to complete
    keyboard.send("command + L") # full screen in Acrobat
    for _ in range(START_PAGE-1):
        keyboard.send("right")
    return

set_up_score(FOLDER, FILE, START_PAGE)
