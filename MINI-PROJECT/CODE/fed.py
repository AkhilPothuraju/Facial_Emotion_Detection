import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model

# Load trained model
model = load_model("D:\MINI-PROJECT\CODE/emotion_model.h5")

# Emotion labels
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

# Start webcam
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Progress bar countdown
start_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(10 - elapsed_time, 0)
    
    # Display countdown timer on screen
    cv2.putText(frame, f"Capturing in {remaining_time} sec", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Real-Time Emotion Detection", frame)
    
    if remaining_time == 0:
        break
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cap.release()
        cv2.destroyAllWindows()
        exit()

# Capture final image
ret, frame = cap.read()
if ret:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (48, 48)) / 255.0
        roi = np.expand_dims(roi, axis=0)
        roi = np.expand_dims(roi, axis=-1)

        # Predict emotion
        preds = model.predict(roi)
        emotion = emotion_labels[np.argmax(preds)]

        # Draw bounding box & label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show captured image with detected emotion
    cv2.imshow("Captured Emotion Detection", frame)
    cv2.waitKey(6000)  # Display result for 3 seconds

cap.release()
cv2.destroyAllWindows()
