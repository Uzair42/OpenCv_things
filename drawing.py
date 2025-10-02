import cv2
import numpy as np

# Drawing parameters
drawing = False
ix, iy = -1, -1
color = (0, 255, 0)
thickness = 3

# Mouse callback function
def draw(event, x, y, flags, param):
    global ix, iy, drawing, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(canvas, (ix, iy), (x, y), color, thickness)
            ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(canvas, (ix, iy), (x, y), color, thickness)

# Open webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    print("Failed to open webcam.")
    exit()

# Create a transparent canvas
canvas = np.zeros_like(frame)

cv2.namedWindow('Live Drawing')
cv2.setMouseCallback('Live Drawing', draw)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Overlay the canvas on the video frame
    overlay = cv2.addWeighted(frame, 0.7, canvas, 0.7, 0)

    # Draw some beautiful shapes for demonstration
    cv2.circle(canvas, (100, 100), 50, (255, 0, 0), 2)
    cv2.rectangle(canvas, (200, 50), (300, 150), (0, 0, 255), 2)
    cv2.ellipse(canvas, (400, 100), (60, 30), 0, 0, 360, (0, 255, 255), 2)

    cv2.imshow('Live Drawing', overlay)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros_like(frame)  # Clear canvas

cap.release()
cv2.destroyAllWindows()