import cv2
import time
import numpy as np

# Load Haar cascade models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Camera started... Running face detection for 10 seconds.")

start_time = time.time()
duration = 10  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

    cv2.putText(frame, "Face Detection Active", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Live Face Detection", frame)

    # Stop after 10 seconds
    if time.time() - start_time > duration:
        break

    # Manual exit option
    if cv2.waitKey(10) & 0xFF == ord('a'):
        break

cap.release()
cv2.destroyAllWindows()

# Show completion message
msg = np.ones((200, 600, 3), dtype=np.uint8) * 255
cv2.putText(msg, "Detection Completed", (80, 120),
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 200, 0), 3)
cv2.imshow("Status", msg)
cv2.waitKey(3000)
cv2.destroyAllWindows()

print("Detection completed and camera turned off.")
