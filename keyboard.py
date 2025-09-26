import cv2
import mediapipe as mp
import numpy as np
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["Space", "<-"] 
]

final_text = ""
delay_counter = 0
def draw_keyboard(img, button_list):
    """Fungsi untuk menggambar keyboard dan highlight tombol."""
    img_new = np.zeros_like(img, np.uint8) 
    for button in button_list:
        x, y = button['pos']
        w, h = button['size']        
        cv2.rectangle(img_new, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button['text'], (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    
    out = img.copy()
    alpha = 0.5
    mask = img_new.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, img_new, 1 - alpha, 0)[mask]
    return out

cap = cv2.VideoCapture(0)
cap.set(3, 1280) 
cap.set(4, 720)  

button_list = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        pos_x = j * 100 + 50
        pos_y = i * 100 + 100
        size = [85, 85]        
        if key == "Space":
            size = [400, 85]
            pos_x = j * 100 + 50
        elif key == "<-":
            pos_x = 550         
        button_list.append({'pos': [pos_x, pos_y], 'size': size, 'text': key})

while True:
    success, img = cap.read()
    if not success:
        break
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = hands.process(img_rgb)
    
    img = draw_keyboard(img, button_list)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            
            
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
            if len(lm_list) != 0:                
                x1, y1 = lm_list[8][1], lm_list[8][2]                
                x2, y2 = lm_list[4][1], lm_list[4][2]               
                cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)                
                for button in button_list:
                    x, y = button['pos']
                    w, h = button['size']
                    if x < x1 < x + w and y < y1 < y + h:                        
                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), 3)                        
                        length = math.hypot(x2 - x1, y2 - y1)            
                        if length < 50 and delay_counter == 0:                            
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button['text'], (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)                            
                            if button['text'] == '<-':
                                final_text = final_text[:-1] 
                            elif button['text'] == 'Space':
                                final_text += " "
                            else:
                                final_text += button['text']                            
                            delay_counter = 1     
    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10: 
            delay_counter = 0
    
    cv2.rectangle(img, (50, 550), (700, 650), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, final_text, (60, 620), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)    
    cv2.imshow("Virtual Keyboard", img)    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()