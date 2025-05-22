import cv2
import dlib
import os
import face_recognition
import numpy as np
from imutils import face_utils
import time

# Load YOLO (using OpenCV DNN with face weights or custom YOLO model)
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

# Dlib for facial landmarks (eye blink detection)
predictor_path = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)
detector = dlib.get_frontal_face_detector()

# Load known faces
known_encodings = []
known_names = []

for file in os.listdir("known_faces"):
    img = face_recognition.load_image_file(f"known_faces/{file}")
    enc = face_recognition.face_encodings(img)
    if enc:
        known_encodings.append(enc[0])
        known_names.append(os.path.splitext(file)[0])

# Eye aspect ratio for liveness detection
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

EYE_AR_THRESH = 0.2
EYE_AR_CONSEC_FRAMES = 3

blink_counter = 0
blinked = False

# Start video capture
cap = cv2.VideoCapture(0)
time.sleep(2.0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # Detect faces using DNN
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dlib_rects = detector(gray, 0)

    # Liveness check: blink detection
    for rect in dlib_rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[36:42]
        rightEye = shape[42:48]
        ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

        if ear < EYE_AR_THRESH:
            blink_counter += 1
        else:
            if blink_counter >= EYE_AR_CONSEC_FRAMES:
                blinked = True
            blink_counter = 0

    # Loop through all detected faces
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.6:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = box.astype("int")
            face = frame[y1:y2, x1:x2]

            # Save captured face
            cv2.imwrite("captured_images/temp.jpg", face)

            # Compare with known faces
            unknown_image = face_recognition.load_image_file("captured_images/temp.jpg")
            unknown_enc = face_recognition.face_encodings(unknown_image)
            if unknown_enc:
                matches = face_recognition.compare_faces(known_encodings, unknown_enc[0])
                face_distances = face_recognition.face_distance(known_encodings, unknown_enc[0])
                best_match_index = np.argmin(face_distances)
                name = "Unknown"
                probability = 0.0

                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    probability = 1 - face_distances[best_match_index]  # Higher is better

                # Display
                label = f"{name}: {probability:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2),
                              (0, 255, 0), 2)

                if blinked:
                    cv2.putText(frame, "Liveness: Passed (Blink Detected)", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                else:
                    cv2.putText(frame, "Liveness: Not Passed", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Face Recognition + Liveness", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
