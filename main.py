import time

import cv2
import numpy as np
import win32gui
from mss import mss

top_list, win_list = [], []
sct = mss()


def enum_cb(hwnd, results):
    win_list.append((hwnd, win32gui.GetWindowText(hwnd)))


def get_beat_saber_bbox():
    win32gui.EnumWindows(enum_cb, top_list)
    beat_saber = [(hwnd, title) for hwnd, title in win_list if 'beat saber' in title.lower()]
    beat_saber = beat_saber[0]
    hwnd = beat_saber[0]
    print(win32gui.GetWindowRect(hwnd))
    return win32gui.GetWindowRect(hwnd)


def screen_record():
    last_time = time.time()
    bbox = None
    while True:
        if bbox is None or (cv2.waitKey(25) & 0xFF == ord('r')):
            bbox = get_beat_saber_bbox()
        print_screen = np.array(sct.grab(bbox))
        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        cv2.imshow('window', print_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    screen_record()
