import cv2
import numpy as np

def detect_uniform(frame):
    # Convert to HSV for color segmentation (example: blue uniform)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define color range for uniform (adjust as needed)
    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Find contours of detected uniform areas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Filter small areas
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, 'Uniform Detected', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    return frame

def main():
    cap = cv2.VideoCapture(0)  # Use webcam
    if not cap.isOpened():
        print("Cannot open camera")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        result = detect_uniform(frame)
        cv2.imshow('Live Uniform Detection', result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()