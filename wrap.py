import cv2
import numpy as np

# Load Haar cascades for face, eyes, and tie detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
# There is no default tie cascade, so we skip tie detection or use a placeholder

def wrap_perspective(frame):
    h, w = frame.shape[:2]
    src = np.float32([[0,0], [w-1,0], [0,h-1], [w-1,h-1]])
    dst = np.float32([[w*0.1,h*0.1], [w*0.9,h*0.2], [w*0.2,h*0.9], [w*0.8,h*0.8]])
    matrix = cv2.getPerspectiveTransform(src, dst)
    wrapped = cv2.warpPerspective(frame, matrix, (w, h))
    return wrapped

def to_green(frame):
    # Convert to grayscale and then to green
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    green = np.zeros_like(frame)
    green[:,:,1] = gray
    return green

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    wrapped = wrap_perspective(frame)
    green_frame = to_green(wrapped)

    gray = cv2.cvtColor(wrapped, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(green_frame, (x, y), (x+w, y+h), (0,255,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = green_frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,255), 2)
        # Tie detection placeholder (draw a rectangle below the face)
        tie_x = x + w//3
        tie_y = y + h
        tie_w = w//3
        tie_h = h//2
        cv2.rectangle(green_frame, (tie_x, tie_y), (tie_x+tie_w, tie_y+tie_h), (255,0,0), 2)

    cv2.imshow('Green Perspective Wrapped Video', green_frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()