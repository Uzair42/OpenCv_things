import cv2
import numpy as np
from datetime import datetime
import logging
import time

# Set up logging
logging.basicConfig(filename='movement_log.txt',
                   level=logging.INFO,
                   format='%(asctime)s - %(message)s')

def detect_finger(frame, hsv):
    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70])
    upper_skin = np.array([20, 255, 255])
    
    # Create mask for skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Apply morphological operations to clean up the mask
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)
    
    # Find contours of the filtered image
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest contour
        max_contour = max(contours, key=cv2.contourArea)
        
        # Find the topmost point of the contour
        top_point = tuple(max_contour[max_contour[:,:,1].argmin()][0])
        return top_point
    return None

def setup_head_detection():
    # Load both face and eye cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    return face_cascade, eye_cascade

def track_heads(frame, face_cascade, eye_cascade, prev_heads):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    current_heads = []
    
    # Draw detailed head tracking
    for (x, y, w, h) in faces:
        center = (x + w//2, y + h//2)
        current_heads.append({
            'center': center,
            'time': time.time(),
            'position': (x, y, w, h)
        })
        
        # Draw detailed head outline
        cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (0, 255, 0), 2)
        
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Detect and draw eyes
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.circle(roi_color, (ex + ew//2, ey + eh//2), ew//2, (0, 0, 255), 2)
        
        # Add person ID and movement info
        cv2.putText(frame, f"ID #{len(current_heads)}", (x, y-25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        
        # Draw movement vector if previous position exists
        if prev_heads and len(prev_heads) >= len(current_heads):
            prev_center = prev_heads[len(current_heads)-1]['center']
            cv2.arrowedLine(frame, prev_center, center, (0, 255, 255), 2)
            
            # Calculate movement speed
            movement = np.sqrt((center[0] - prev_center[0])**2 + 
                             (center[1] - prev_center[1])**2)
            if movement > 5:
                cv2.putText(frame, f"Speed: {movement:.0f}px/f", 
                           (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (0, 255, 255), 2)
                logging.info(f"Person #{len(current_heads)} moved {movement:.2f} pixels")

    # Add group statistics
    if len(faces) > 0:
        cv2.putText(frame, f"Total People: {len(faces)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Active Tracking: {'Yes' if len(faces) > 0 else 'No'}", 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Draw crowd density heat map
    if len(faces) > 3:
        heat_map = np.zeros_like(frame)
        for head in current_heads:
            x, y = head['center']
            cv2.circle(heat_map, (x, y), 50, (0, 0, 255), -1)
        frame = cv2.addWeighted(frame, 0.7, heat_map, 0.3, 0)

    return frame, current_heads

def main():
    cap = cv2.VideoCapture(0)
    face_cascade, eye_cascade = setup_head_detection()
    
    # Create a black canvas
    canvas = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Initialize variables
    current_color = (0, 255, 0)  # Start with green
    last_point = None
    drawing = False
    prev_heads = []
    
    print("Controls:")
    print("R - Red")
    print("G - Green")
    print("B - Blue")
    print("Y - Yellow")
    print("W - White")
    print("C - Clear canvas")
    print("Space - Toggle drawing")
    print("Q - Quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        
        # Enhanced head detection and tracking
        frame, current_heads = track_heads(frame, face_cascade, eye_cascade, prev_heads)
        prev_heads = current_heads

        # Display head count
        cv2.putText(frame, f"People Count: {len(current_heads)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Convert to HSV for finger detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Finger detection and drawing
        finger_point = detect_finger(frame, hsv)
        
        if finger_point and drawing:
            if last_point is not None:
                cv2.line(canvas, last_point, finger_point, current_color, 5)
            last_point = finger_point
        else:
            last_point = None
        
        # Combine frame and canvas
        display = cv2.addWeighted(frame, 1.0, canvas, 0.7, 0)
        
        # Draw current color indicator
        cv2.circle(display, (30, 60), 20, current_color, -1)
        
        cv2.imshow("Head Detection and Finger Paint", display)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            current_color = (0, 0, 255)  # Red
        elif key == ord('g'):
            current_color = (0, 255, 0)  # Green
        elif key == ord('b'):
            current_color = (255, 0, 0)  # Blue
        elif key == ord('y'):
            current_color = (0, 255, 255)  # Yellow
        elif key == ord('w'):
            current_color = (255, 255, 255)  # White
        elif key == ord('c'):
            canvas = np.zeros((480, 640, 3), dtype=np.uint8)
        elif key == 32:  # Space bar
            drawing = not drawing
            print("Drawing:", "On" if drawing else "Off")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()