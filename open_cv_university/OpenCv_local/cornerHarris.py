import cv2 as cv
import numpy as np

# --- 1. Setup Video Capture (adjust index if needed, e.g., 0 or 1) ---
cap = cv.VideoCapture(0) 

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Optional: Check if frame is entirely black (e.g. if camera is slow to start)
    # if np.mean(frame) < 1.0: 
    #     continue

    # --- 2. Convert frame to grayscale and float32 ---
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    # --- 3. Apply Harris Corner Detector ---
    # The parameters in your code (21, 3, 0.04) are valid for blockSize, ksize, and k respectively.
    dst = cv.cornerHarris(gray, 21, 3, 0.04)

    # --- 4. Dilate the result to emphasize corners (optional but helpful) ---
    dst = cv.dilate(dst, None)
    # print(dst)

    # --- 5. Threshold the corner response and mark corners on the original color frame ---
    # Optimal threshold value might vary. 0.01 * dst.max() is a common starting point.
    frame[dst > 0.1 * dst.max()] = [0, 140, 255] # Mark corners 

    # --- 6. Display the result ---
    cv.imshow('Harris Corners', frame)

    # --- 7. Break the loop when 'q' is pressed ---
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv.destroyAllWindows()
