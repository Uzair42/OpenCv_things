import cv2
import numpy as np

# Open the first camera (cam 1)
cap = cv2.VideoCapture(0)


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for consistency
    frame = cv2.resize(frame, (640, 480))

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Change thickness of edges by dilating
    kernel = np.ones((3, 3), np.uint8)
    thick_edges = cv2.dilate(edges, kernel, iterations=2)

    # Warp the image (e.g., perspective transform)
    rows, cols = thick_edges.shape
    pts1 = np.float32([[0,0],[cols-1,0],[0,rows-1],[cols-1,rows-1]])
    pts2 = np.float32([[20,20],[cols-20,30],[30,rows-20],[cols-30,rows-30]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(thick_edges, M, (cols, rows))

    # Convert single channel to BGR for saving
    warped_bgr = cv2.cvtColor(warped, cv2.COLOR_GRAY2BGR)

    # Show the result
    cv2.imshow('Warped Edges', warped_bgr)

    # Write the frame
    out.write(warped_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()