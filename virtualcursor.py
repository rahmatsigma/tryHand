import cv2
import mediapipe as mp
import pyautogui
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

click_down = False  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                px, py = int(lm.x * w), int(lm.y * h)
                lm_list.append((px, py))

            x_index, y_index = lm_list[8]
            x_thumb, y_thumb = lm_list[4]

            screen_x = int(handLms.landmark[8].x * screen_w)
            screen_y = int(handLms.landmark[8].y * screen_h)
            pyautogui.moveTo(screen_x, screen_y, duration=0.1)
            cv2.circle(frame, (x_index, y_index), 10, (255, 0, 255), cv2.FILLED)

            distance = math.hypot(x_index - x_thumb, y_index - y_thumb)
            if distance < 40:
                if not click_down:  
                    click_down = True
                    pyautogui.click()
                    cv2.circle(frame, (x_index, y_index), 15, (0, 255, 0), cv2.FILLED)
            else:
                click_down = False

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Virtual Cursor + Click", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
