import cv2
import mediapipe as mp
import numpy as np
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Helper function to count fingers
def count_fingers(hand_landmarks, hand_label):
    finger_tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_label == "Right":
        fingers.append(hand_landmarks.landmark[finger_tips_ids[0]].x < hand_landmarks.landmark[finger_tips_ids[0] - 1].x)
    else:
        fingers.append(hand_landmarks.landmark[finger_tips_ids[0]].x > hand_landmarks.landmark[finger_tips_ids[0] - 1].x)

    # Other fingers
    for tip_id in finger_tips_ids[1:]:
        fingers.append(hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y)

    return fingers.count(True)

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        total_fingers = 0

        if results.multi_hand_landmarks:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = hand_handedness.classification[0].label
                fingers_open = count_fingers(hand_landmarks, hand_label)
                total_fingers += fingers_open

                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255,0,0), thickness=2))

        cv2.putText(frame, f'Fingers Open: {total_fingers}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Initialize VideoWriter after getting frame size
        if out is None:
            out = cv2.VideoWriter('hand_finger_count.avi', fourcc, 20.0, (w, h))

        out.write(frame)
        cv2.imshow('Hand and Finger Tracking', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

cap.release()
if out:
    out.release()
cv2.destroyAllWindows()