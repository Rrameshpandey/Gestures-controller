import cv2 as cv

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
    cv.imshow("live recording", frame)
    if cv.waitKey(1) == ord("q"):
        print("live recording is stopped")
        break
cap.release()
cv.destroyAllWindows()