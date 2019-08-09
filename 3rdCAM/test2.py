import cv2

capture = cv2.VideoCapture(0)
#capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    ret, frame = capture.read()
    cv2.imshow("VideoFrame", frame)
    print(capture.)
    if cv2.waitKey(1) > 0: break

capture.release()
cv2.destroyAllWindows()

