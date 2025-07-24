# Import required libraries
import pickle

import cv2
import mediapipe as mp
import numpy as np

# Load trained model
model_dict = pickle.load(open("EnglishHandSignModel.p", "rb"))
model = model_dict["model"]

# Get camera feed (camera index 2)
cap = cv2.VideoCapture(2)

# Prepare MediaPipe hand detection tools
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize hand detection model
# static_image_mode=True: Detect hands in each frame
# min_detection_confidence=0.3: Accept detections with 30% or higher confidence
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Letter labels dictionary (Class number -> Letter mapping)
labels_dict = {0: "A", 1: "B", 2: "L"}

# Process camera feed in infinite loop
while True:
    # Create new data lists for each frame
    data_aux = []  # List to store hand features
    x_ = []  # List to store x coordinates
    y_ = []  # List to store y coordinates

    # Read a frame from camera
    ret, frame = cap.read()

    # Get frame dimensions
    H, W, _ = frame.shape

    # Convert BGR to RGB (MediaPipe expects RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform hand detection
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw detected hand
            mp_drawing.draw_landmarks(
                frame,  # Image to draw on
                hand_landmarks,  # Hand landmarks
                mp_hands.HAND_CONNECTIONS,  # Hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )

        for hand_landmarks in results.multi_hand_landmarks:
            # Collect coordinates of hand landmarks
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            # Calculate normalized coordinates
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))  # X coordinate normalization
                data_aux.append(y - min(y_))  # Y coordinate normalization

        # Calculate coordinates for drawing rectangle around hand
        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10
        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        # Make prediction with model
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = labels_dict[int(prediction[0])]

        # Draw prediction result on image
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)  # Rectangle around hand
        cv2.putText(
            frame,
            predicted_character,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (0, 0, 0),
            3,
            cv2.LINE_AA,
        )  # Predicted letter

    # Display image
    cv2.imshow("frame", frame)
    cv2.waitKey(1)

# Release resources when program ends
cap.release()
cv2.destroyAllWindows()
