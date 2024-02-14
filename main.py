import cv2
import threading
from deepface import DeepFace
import tempfile
import os

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

face_match = False

reference_img = cv2.imread("elya.jpg")


def check_face(img_frame):
    global face_match
    try:
        # Save the current frame as a temporary image file
        _, temp_img_path = tempfile.mkstemp(suffix=".jpg")
        cv2.imwrite(temp_img_path, img_frame)

        # Perform face recognition
        result = DeepFace.verify(img1_path=temp_img_path, img2_path="elya.jpg")

        # Check if the faces match
        if result["distance"] < 0.9:
            face_match = True
        else:
            face_match = False

        # Remove the temporary image file
        os.remove(temp_img_path)

    except ValueError:
        face_match = False


while True:
    ret, frame = cap.read()

    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                ...
        counter += 1

        if face_match:
            cv2.putText(frame, "Matched", (20, 450), cv2.FONT_ITALIC, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "Not Match", (20, 450), cv2.FONT_ITALIC, 2, (0, 0, 255), 3)

        cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
