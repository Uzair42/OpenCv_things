import cv2 as cv
# Load the pre-trained Haar Cascade classifiers for face and eye detection
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')

# Open the default webcam
cap = cv.VideoCapture(0)

# Define the codec and create VideoWriter object to save the video in grayscale
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output_bw.avi', fourcc, 20.0, (640, 480), isColor=False)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv.rectangle(gray, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)

    # Show the grayscale frame with rectangles
    cv.imshow('Eye Tracker (Grayscale)', gray)

    # Write the grayscale frame to the output video
    out.write(gray)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()