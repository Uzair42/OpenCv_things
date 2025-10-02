import cv2

# Load pre-trained model and class labels (using MobileNet SSD and COCO labels)
prototxt = cv2.data.haarcascades + "deploy.prototxt.txt"
model = cv2.data.haarcascades + "res10_300x300_ssd_iter_140000_fp16.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# COCO class labels for MobileNet SSD (subset)
CLASSES = ["background", "person", "bicycle", "car", "motorcycle", "airplane", "bus",
           "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign",
           "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
           "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag",
           "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
           "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
           "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
           "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
           "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table",
           "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
           "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock",
           "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

# Read image from camera or file
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or replace with filename

while True:
    ret, frame = cap.read()
    if not ret:
        print("No frame captured")
        break

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    found = False
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            if idx < len(CLASSES):
                label = CLASSES[idx]
            else:
                label = "Unknown"
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            found = True

    if not found:
        cv2.putText(frame, "No objects detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Object Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()