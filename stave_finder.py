import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

from PIL import Image


def plot_hlines(im, lines, color='blue'):
    W = im.shape[1]
    for i in range(len(lines)):
        x = [0, W-1]
        y = [lines[i], lines[i]]
        plt.plot(x, y, color=color, linewidth=0.5)
    plt.imshow(im)
    plt.show()

def find_staff_lines(im_bin, window = 3, thresh=0.2):
    H = im_bin.shape[0]
    staff_lines = (np.mean(im_bin, axis=1) < thresh).nonzero()[0]
    whiteness = np.mean(im_bin, axis=0)
    start_x = np.argmin(whiteness)
    dif = im_bin[1:H, start_x] - im_bin[:H-1, start_x]
    dif_i = (dif != 0).nonzero()[0]

    border_lines = []
    for i in range(len(dif_i)):
        closest = np.argmin((staff_lines - dif_i[i])**2)
        if (staff_lines[closest] - dif_i[i])**2 < window**2:
            border_lines.append(staff_lines[closest])
    # plot_hlines(im_bin, border_lines, color='red')
    return border_lines

def find_seps(im_bin, border_lines):
    seps = []
    i = 1
    while i < len(border_lines)-1:
        e, s = border_lines[i], border_lines[i+1]
        dark = 1 - np.mean(im_bin[e: s], axis=1)
        dist = (np.arange(e, s) - (e + s)//2)**2 / ((e+s)//2)**2
        seps.append(e+np.argmin(dark + dist))
        i += 2
    return seps

def sep_im(file_path, count=1):
    im = cv2.imread(file_path)
    thresh = 0.5
    im_bin = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    im_bin = cv2.threshold(im_bin*1.0/255, thresh, 1.0, cv2.THRESH_BINARY)[1]

    border_lines = find_staff_lines(im_bin)
    # plot_hlines(im_bin, border_lines)
    seps = find_seps(im_bin, border_lines)
    # plot_hlines(im_bin, seps)

    staves = np.split(im, seps, axis=0)
    for i in range(len(staves)):       
        cv2.imwrite('stave' + str(count) + '.png', staves[i])
        count += 1
    return count

def sep_folder(root, base_name):
    count = 1
    im_names = sorted([file for file in os.listdir(root)
                       if file.endswith('.png') and file.startswith(base_name)])
    for file_name in im_names:
        file_path = root + file_name
        count = sep_im(file_path, count) 
    return True


base_name = 'violin_sonata'
root = './'

sep_folder(root, base_name)




