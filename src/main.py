import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from drawer import *
import time
from config import *
from controller import *
from gestures import *
from fps import FPS
# from utilis import *

model_path = model_path
base_options = python.BaseOptions(model_asset_path = model_path)
options = vision.HandLandmarkerOptions(base_options = base_options,
                                       num_hands =1,
                                       min_hand_detection_confidence = 0.7,
                                       running_mode = vision.RunningMode.VIDEO)
landmarker = vision.HandLandmarker.create_from_options(options)
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
fps_counter = FPS()
while True:
    ref, frame = cap.read()
    if not ref:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = cv.flip(frame, 1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = rgb_frame)
    timestamp_mp = int(time.time()*1000)
    result = landmarker.detect_for_video(mp_image, timestamp_mp)
    if result.hand_landmarks:
        hand = result.hand_landmarks[0]
        raw_label = result.handedness[0][0].category_name
        hand_label = "Left" if raw_label == "Right" else "Right"
        # print(hand_label)
        height,width,_ = frame.shape
        for h in result.hand_landmarks:
            draw_landmarks(frame, h, width, height, result)
        # if is_index_up(hand):
        #     text = "INDEX UP"
        # else:
        #     text = "INDEX DOWN"
        # cv.putText(frame, text, (40,80), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2 )
        # states = finger_state(hand)
        fps = fps_counter.get_fps()
        gestures = recognize_gesture(hand, hand_label)
        handle_drag(gestures)
        if gestures in ["Pointing", "Fist"]:
            move_mouse(hand)
        handle_click(gestures)
        if gestures == "Open Palm":
            handle_scroll(hand)
        else:
            reset_scroll()

        # print("click")
        # thumb_gestures = distance(hand, 4, 8)
        # if thumb_gestures < 0.05:
        #     gestures = "OK"
        draw__info(frame,[f"Gestures: {gestures}",
                          f"FPS:{fps}",
                          f"Hand: {hand_label}"])
    else:
        pass
    cv.imshow("live recording",frame)
    if cv.waitKey(1) == ord("q"):
        print("live recording is stopped")
        break
cap.release()
cv.destroyAllWindows()
landmarker.close()