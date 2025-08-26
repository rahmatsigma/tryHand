import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class HandDetection:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def findHandLandMarks(self, image, draw=True):
        original_image = image.copy()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        all_landmarks_list = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, _ = original_image.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    landmarks_list.append((id, x, y))
                all_landmarks_list.append(landmarks_list)

                if draw:
                    mp_drawing.draw_landmarks(original_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        return all_landmarks_list, original_image
