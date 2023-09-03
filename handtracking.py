import cv2
import mediapipe as mp
import serial #install pyserial
import time

arduino = serial.Serial(port = 'COM3',baudrate=9600, timeout=0)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe drawing module for visualization
mp_drawing = mp.solutions.drawing_utils

# Initialize OpenCV webcam capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the frame to RGB for MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(frame_rgb)

    # Initialize a list to store finger states (0 for open, 1 for closed)
    finger_states = [0, 0, 0, 0, 0]

    # If hands are detected, draw landmarks on the frame and analyze finger states
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Compare the horizontal position of the thumb landmarks
            thumb_tip_x = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
            thumb_second_x = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x

            # Compare the vertical position of the fingertips and the base of the fingers
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            index_base = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

            middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            middle_base = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

            ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
            ring_base = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y

            pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
            pinky_base = landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y

            # Check if fingers are open or closed based on horizontal positions
            if thumb_tip_x > thumb_second_x:
                finger_states[0] = 1  # Thumb is closed
            if index_tip < index_base:
                finger_states[1] = 1  # Index finger is closed
            if middle_tip < middle_base:
                finger_states[2] = 1  # Middle finger is closed
            if ring_tip < ring_base:
                finger_states[3] = 1  # Ring finger is closed
            if pinky_tip < pinky_base:
                finger_states[4] = 1  # Pinky is closed

    # Display the finger states on the frame
    cv2.putText(frame, f'Finger States: {finger_states}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Print the finger states to the console
    print(f'Finger States: {finger_states}')
    # Print to serial the new states
    result = ''.join(str(item) for item in finger_states)
    print(result)
    arduino.write(bytes(result, 'utf-8'))
    time.sleep(2)

    # Display the frame
    cv2.imshow("Hand Tracking", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
