import cv2
import numpy as np

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

def main():
    cap = cv2.VideoCapture(0)
    
    # Create a black canvas
    canvas = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Initialize variables
    current_color = (0, 255, 0)  # Start with green
    last_point = None
    drawing = False
    
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
            
        # Flip frame horizontally for natural movement
        frame = cv2.flip(frame, 1)
        
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detect finger tip
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
        cv2.circle(display, (30, 30), 20, current_color, -1)
        
        cv2.imshow("Finger Paint", display)
        
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