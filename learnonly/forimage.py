# Step 1: Import the necessary modules
import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# step 2: initialize the model path
model_path = "docs/hand_landmarker.task"

# step 3: Create an handlandmarker objects
base_options = python.BaseOptions(model_asset_path = model_path)
options = vision.HandLandmarkerOptions(base_options = base_options,
                                       num_hands = 1,
                                       running_mode = vision.RunningMode.IMAGE)
detector = vision.HandLandmarker.create_from_options(options)
# print("Hand Landmarker is initialized successfully!")
# Step 4: Load the image from you local directory
image = mp.Image.create_from_file("docs/image.png")
# Step 5: Detect the hand landmarks from the image
det_result = detector.detect(image)
# # print(det_result) long output, only print the number of detected hand
# '''only printed the number of detected hand'''
# # print("Hand detection:", len(det_result.hand_landmarks))
if det_result.hand_landmarks:
    hand = det_result.hand_landmarks[0]
    image_np = image.numpy_view().copy()
    height, width, _ = image_np.shape
    for hand in det_result.hand_landmarks:
        for landmark in hand:
            x=int(landmark.x * width)
            y=int(landmark.y * height)
            cv.circle(image_np, (x,y),5,(0,255,0),-1)
# coordinates to make a handconnection and show skeleton in handlandmark 
            HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),

    (0,5),(5,6),(6,7),(7,8),

    (0,9),(9,10),(10,11),(11,12),

    (0,13),(13,14),(14,15),(15,16),

    (0,17),(17,18),(18,19),(19,20),

    (5,9),(9,13),(13,17)
]
            for startIdx, endIdx in HAND_CONNECTIONS:
                start = hand[startIdx]
                end = hand[endIdx]
                x1 = int(start.x *width)
                y1 = int(start.y *height)
                x2 = int(end.x *width)
                y2 = int(end.y *height)
                cv.line(image_np,(x1,y1),(x2,y2),(255,0,0),2)
cv.imshow("Hand Landmarks", image_np)
cv.waitKey(0)
cv.destroyAllWindows()



