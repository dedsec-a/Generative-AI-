import cv2
import face_recognition
import numpy as np
import os
import dlib
from scipy.spatial import distance as dist
from ultralytics import YOLO

# ----------- Eye Aspect Ratio Functions -----------

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def is_blinking(landmarks):
    leftEye = np.array([[landmarks.part(n).x, landmarks.part(n).y] for n in range(36, 42)])
    rightEye = np.array([[landmarks.part(n).x, landmarks.part(n).y] for n in range(42, 48)])
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    return (leftEAR + rightEAR) / 2.0

# ----------- Load Known Faces -----------
known_face_encodings = []
known_face_names = []

for file in os.listdir("known_faces"):
    if file.endswith(".jpg") or file.endswith(".png"):
        img = face_recognition.load_image_file(f"known_faces/{file}")
        encodings = face_recognition.face_encodings(img)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(file)[0])

# ----------- Load YOLO and dlib predictor -----------
model = YOLO("yolov8n-face.pt")
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# ----------- Initialize -----------
cap = cv2.VideoCapture(0)
EYE_AR_THRESH = 0.23
EYE_AR_CONSEC_FRAMES = 2
blink_counter = {}
blink_confirmed = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)[0]

    for r in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = map(int, r[:6])
        face_img = frame[y1:y2, x1:x2]
        rgb_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb_face)
        name = "Unknown"
        live_status = False

        if encodings:
            match = face_recognition.compare_faces(known_face_encodings, encodings[0])
            face_distances = face_recognition.face_distance(known_face_encodings, encodings[0])
            best_match_index = np.argmin(face_distances)

            if match[best_match_index]:
                name = known_face_names[best_match_index]

                # Run liveness detection
                face_rect = dlib.rectangle(0, 0, face_img.shape[1], face_img.shape[0])
                landmarks = predictor(rgb_face, face_rect)
                ear = is_blinking(landmarks)

                if name not in blink_counter:
                    blink_counter[name] = 0
                    blink_confirmed[name] = False

                if ear < EYE_AR_THRESH:
                    blink_counter[name] += 1
                else:
                    if blink_counter[name] >= EYE_AR_CONSEC_FRAMES:
                        blink_confirmed[name] = True
                    blink_counter[name] = 0

                live_status = blink_confirmed[name]

        label = f"{name} - {'Live' if live_status else 'Spoof' if name != 'Unknown' else 'Unknown'}"
        color = (0, 255, 0) if live_status else (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Secure Face Access System", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
