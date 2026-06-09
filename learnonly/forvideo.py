import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
model_path = "docs/hand_landmarker.task"
base_options = python.BaseOptions(model_asset_path =model_path)
options = vision.HandLandmarkerOptions(base_options =base_options,
                                       num_hands =1,
                                       min_hand_detection_confidence = 0.5,
                                       running_mode = vision.RunningMode.VIDEO)
landmarker = vision.HandLandmarker.create_from_options(options)
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open Camera")
    exit()
while True:
    ref, frame =cap.read()
    if not ref:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = cv.flip(frame,1)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = rgb_frame)
    timestamp_mp = int(time.time()*1000)
    result = landmarker.detect_for_video(mp_image, timestamp_mp)
    if result.hand_landmarks:
        hand = result.hand_landmarks[0]
        height, width, _ = frame.shape
        for hand in result.hand_landmarks:
            for landmark in hand:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                cv.circle(frame, (x,y), 6, (0,255,0), -1)
                cv.putText(frame, f"Hands: {len(result.hand_landmarks)}", (20,40), cv.FONT_HERSHEY_SIMPLEX,
                           1, (0,255,0),2)
                Hand_connections =[
                    (0,1),(1,2),(2,3),(3,4),
                    (0,5), (5,6),(6,7),(7,8),
                    (0,9),(9,10),(10,11),(11,12),
                    (0,13),(13,14),(14,15),(15,16),
                    (0,17),(17,18),(18,19),(19,20),
                    (5,9),(9,13),(13,17)
                ]
                for start_Idx, end_Idx in Hand_connections:
                    start = hand[start_Idx]
                    end = hand[end_Idx]
                    x1 = int(start.x *width)
                    y1 = int(start.y *height)
                    x2 = int(end.x *width)
                    y2 = int(end.y *height)
                    cv.line(frame, (x1,y1), (x2,y2), (255,0,0), 2)
    cv.imshow("live Recording", frame)
    if cv.waitKey(1) == ord("q"):
        print("live recording is stopped")
        break
cap.release()
cv.destroyAllWindows()
landmarker.close()