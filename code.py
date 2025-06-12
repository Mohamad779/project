import cv2
import numpy as np
import mediapipe as mp
import serial
import time

# serial port – adjust to yours
s = serial.Serial('COM9', 9600, timeout=1)

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(static_image_mode=False,
                             max_num_faces=1,
                             refine_landmarks=True,
                             min_detection_confidence=0.5,
                             min_tracking_confidence=0.5)

# indices for left/right eye in MediaPipe FaceMesh
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(landmarks, pts):
    # compute vertical/horizontal distances
    a = np.linalg.norm(landmarks[pts[1]] - landmarks[pts[5]])
    b = np.linalg.norm(landmarks[pts[2]] - landmarks[pts[4]])
    c = np.linalg.norm(landmarks[pts[0]] - landmarks[pts[3]])
    return (a + b) / (2.0 * c)

cap = cv2.VideoCapture(0)
sleep = drowsy = active = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(img_rgb)

    status = ""
    color = (0, 255, 0)

    if result.multi_face_landmarks:
        mesh = result.multi_face_landmarks[0]
        h, w, _ = frame.shape
        pts = [(int(p.x * w), int(p.y * h)) for p in mesh.landmark]

        left_ear = eye_aspect_ratio(np.array(pts), LEFT_EYE)
        right_ear = eye_aspect_ratio(np.array(pts), RIGHT_EYE)

        # tuned thresholds
        if left_ear < 0.2 and right_ear < 0.2:
            sleep += 1; drowsy = active = 0
            if sleep > 6:
                s.write(b'a'); time.sleep(0.1)
                status, color = "SLEEPING !!!", (0, 0, 255)

        elif left_ear < 0.25 or right_ear < 0.25:
            drowsy += 1; sleep = active = 0
            if drowsy > 6:
                s.write(b'a'); time.sleep(0.1)
                status, color = "Drowsy !", (0, 0, 255)

        else:
            active += 1; sleep = drowsy = 0
            if active > 6:
                s.write(b'b'); time.sleep(0.1)
                status, color = "Active :)", (0, 255, 0)

        # draw status
        cv2.putText(frame, status, (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Blink Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
