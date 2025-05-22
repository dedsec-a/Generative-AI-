import face_recognition
import cv2
import numpy as np
import os

# -------------------------
# Step 1: Register user
# -------------------------
print("[INFO] Starting camera for registration...")
video_capture = cv2.VideoCapture(0)

print("[INFO] Please look at the camera to register your face.")
while True:
    ret, frame = video_capture.read()
    cv2.imshow('Registration - Press "s" to save your face', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("registered_user.jpg", frame)
        print("[INFO] Face saved as 'registered_user.jpg'")
        break

video_capture.release()
cv2.destroyAllWindows()

# Load and encode registered face
registered_image = face_recognition.load_image_file("registered_user.jpg")
registered_face_encodings = face_recognition.face_encodings(registered_image)

if not registered_face_encodings:
    print("[ERROR] No face found in the registration image.")
    exit()

known_face_encoding = registered_face_encodings[0]

# -------------------------
# Step 2: Start verification loop
# -------------------------
print("[INFO] Starting real-time face recognition...")
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Faster processing
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        match = face_recognition.compare_faces([known_face_encoding], face_encoding, tolerance=0.45)
        name = "Unknown"

        if match[0]:
            name = "Access Granted"
            color = (0, 255, 0)
        else:
            name = "Access Denied"
            color = (0, 0, 255)

        # Scale back up for original frame
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow('Face Verification System', frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

