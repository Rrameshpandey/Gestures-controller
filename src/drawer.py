import cv2 as cv
from connection import Hand_connections

def draw_landmarks(frame, hand, width, height, result):
    for landmark in hand:
        x = int(landmark.x *width)
        y = int(landmark.y *height)
        cv.circle(frame, (x,y), 6, (0,255,0), -1)
        cv.putText(frame, f"Hands: {len(result.hand_landmarks)}", (20,40), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0,255,0),2)
        for start_Idx, end_Idx in Hand_connections:
            start = hand[start_Idx]
            end =hand[end_Idx]
            x1 = int(start.x *width)
            y1 = int(start.y *height)
            x2 = int(end.x *width)
            y2 = int(end.y *height)
            cv.line(frame,(x1,y1), (x2,y2), (255,0,0),2)
