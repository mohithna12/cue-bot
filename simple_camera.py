import cv2

print("Testing camera...")

# Try camera 0
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("Camera 0 opened")
    ret, frame = cap.read()
    if ret:
        print("Frame captured successfully")
        cv2.imshow("Camera 0", frame)
        print("Press 'q' to quit")
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        print("No frame captured")
else:
    print("Camera 0 failed")

cap.release()
cv2.destroyAllWindows()
print("Done")
