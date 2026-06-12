import pyautogui
from config import *

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
screen_w, screen_h = pyautogui.size()
pre_x = screen_w // 2
pre_y = screen_h // 2
def move_mouse(hand):
    global pre_x,pre_y
    x = hand[8].x
    y = hand[8].y

    x = max(FRAME_X_MIN, min(x, FRAME_X_MAX))
    y = max(FRAME_Y_MIN, min(y, FRAME_Y_MAX))

    move_x = int(
    (x - FRAME_X_MIN)
    / (FRAME_X_MAX - FRAME_X_MIN)
    * screen_w
)

    move_y = int(
    (y - FRAME_Y_MIN)
    / (FRAME_Y_MAX - FRAME_Y_MIN)
    * screen_h
)
    smooth_x = pre_x + (move_x - pre_x) * SMOOTHING_FACTOR
    smooth_y = pre_y + (move_y - pre_y) * SMOOTHING_FACTOR
    pyautogui.moveTo(smooth_x, smooth_y)

    pre_x = smooth_x
    pre_y = smooth_y


last_gesture = ""
def handle_click(gestures):
    global last_gesture
    if gestures == "OK" and last_gesture != "OK":
        pyautogui.click()
    elif gestures == "Victory" and last_gesture != "Victory":
        pyautogui.rightClick()
    last_gesture = gestures



pre_scroll_y = None
def handle_scroll(hand):
    global pre_scroll_y
    curr_y = hand[8].y
    if pre_scroll_y is None:
        pre_scroll_y = curr_y
        return
    dy = curr_y - pre_scroll_y
    pre_scroll_y = curr_y
    if dy < - Scroll_Threshold:
        pyautogui.scroll(Scroll_amount)
    elif dy> Scroll_Threshold:
        pyautogui.scroll(- Scroll_amount)
def reset_scroll():
    global pre_scroll_y
    pre_scroll_y = None



dragging = False
def handle_drag(gestures):
    global dragging
    if gestures == "Fist" and not dragging:
        pyautogui.mouseDown()
        dragging = True
    elif gestures != "Fist" and dragging:
        pyautogui.mouseUp()
        dragging = False 