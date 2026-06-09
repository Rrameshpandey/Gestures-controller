import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from drawer import draw_landmarks
import time

model_path = "docs/hand_landmarker.task"
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
        height,width,_ = frame.shape
        for hand in result.hand_landmarks:
            draw_landmarks(frame, hand, width, height, result)
    cv.imshow("live recording", frame)
    if cv.waitKey(1) == ord("q"):
        print("live recording is stopped")
        break
cap.release()
cv.destroyAllWindows()
landmarker.close()