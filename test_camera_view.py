import cv2

print("Testing camera 0...")
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("Camera 0 opened")
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Camera 0 Test", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("No frame")
            break
else:
    print("Camera 0 failed")

cap.release()
cv2.destroyAllWindows()
