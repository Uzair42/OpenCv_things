import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to calculate angle between 3 points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Start video capture
cap = cv2.VideoCapture(0)
pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)

prev_time = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame color (BGR to RGB)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.pose_landmarks:
        # Draw landmarks and connections
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
        )

        landmarks = results.pose_landmarks.landmark

        # Extract landmark coordinates
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        # Calculate angles
        elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

        # Determine posture
        posture = "Standing"
        if knee_angle < 120:
            posture = "Sitting"
        elif elbow_angle < 60:
            posture = "Leaning"

        # Display posture and angles
        cv2.putText(image, f'Posture: {posture}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.putText(image, f'Elbow Angle: {int(elbow_angle)}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.putText(image, f'Knee Angle: {int(knee_angle)}', (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        # Print details in console
        print(f"[LOG] Posture: {posture} | Elbow: {int(elbow_angle)}° | Knee: {int(knee_angle)}°")

    # FPS counter
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time
    cv2.putText(image, f'FPS: {int(fps)}', (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    # Show the frame
    cv2.imshow('Pose Detection - MediaPipe', image)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

pose.close()
cap.release()
cv2.destroyAllWindows()
