import cv2
import mediapipe as mp
import requests # type: ignore
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Replace with your ESP32-CAM's IP address
stream_url = "http://192.168.0.11/picture"
led_url_base = "http://192.168.0.11/led?state="

prev_state = None  # Track LED state to reduce unnecessary HTTP calls

while True:
    try:
        # Fetch the image from the ESP32-CAM
        response = requests.get(stream_url, stream=True)
        if response.status_code == 200:
            # Convert the image to a NumPy array
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # Flip the frame vertically (optional)
            frame = cv2.flip(frame, 0)

            # Convert the frame to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe Hands
            results = hands.process(rgb_frame)

            # Draw hand landmarks on the frame
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                    )
                # Hand detected: turn LED ON if not already on
                if prev_state != "on":
                    requests.get(led_url_base + "on")
                    prev_state = "on"
            else:
                # No hand detected: turn LED OFF if not already off
                if prev_state != "off":
                    requests.get(led_url_base + "off")
                    prev_state = "off"

            # Display the frame
            cv2.imshow("ESP32-CAM Hand Detection", frame)

            # Press 'q' to exit
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            print("Failed to fetch image from ESP32-CAM")
            break
    except Exception as e:
        print(f"Error: {e}")
        break

# Release resources
hands.close()
cv2.destroyAllWindows()
