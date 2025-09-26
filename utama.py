import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from handDetection import HandDetection
from playsound import playsound 
import threading 

def play_audio(sound_file):
    try:
        playsound(sound_file)
    except Exception as e:
        print(f"Error playing sound: {e}")

cap = cv2.VideoCapture(0)
detector = HandDetection()

tip_ids = [4, 8, 12, 16, 20]

gesture_names = {
    0: "Fist ✊",
    1: "One ☝️",
    2: "Peace ✌️",
    3: "Three 🤟",
    4: "Four ✋",
    5: "Hallo 🖐️"
}

# BARU: Dictionary untuk file suara
gesture_sounds = {
    0: "sounds/fist.mp3",
    1: "sounds/one.mp3",
    2: "sounds/peace.mp3",
    3: "sounds/three.mp3",
    4: "sounds/four.mp3",
    5: "sounds/hallo.mp3"
}

colors = {
    0: (0, 0, 255),
    1: (0, 128, 255),
    2: (0, 255, 0),
    3: (255, 255, 0),
    4: (255, 0, 0),
    5: (128, 0, 128),
}

FONT_PATH = "seguiemj.ttf"

last_gestures = {}

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not success:
        break

    landmarks_list, output_frame = detector.findHandLandMarks(frame, draw=True)

    if not landmarks_list:
        last_gestures.clear()

    if landmarks_list:
        img_pil = Image.fromarray(cv2.cvtColor(output_frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        try:
            font = ImageFont.truetype(FONT_PATH, 48)
        except IOError:
            font = ImageFont.load_default()

        for i, landmarks in enumerate(landmarks_list):
            fingers = []

            if landmarks[tip_ids[0]][1] > landmarks[tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if landmarks[tip_ids[id]][2] < landmarks[tip_ids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = sum(fingers)
            gesture = gesture_names.get(total_fingers, "Unknown")
            color = colors.get(total_fingers, (255, 255, 255))
            if last_gestures.get(i) != total_fingers:
                sound_file = gesture_sounds.get(total_fingers)
                if sound_file:
                    threading.Thread(target=play_audio, args=(sound_file,), daemon=True).start()
                last_gestures[i] = total_fingers

            x_offset = 50
            y_offset = 100 + i * 100
            draw.rectangle((x_offset - 10, y_offset - 10, x_offset + 400, y_offset + 60), fill=color)
            draw.text((x_offset, y_offset), f"Hand {i+1}: {gesture}", font=font, fill=(0, 0, 0))

        output_frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    cv2.imshow("Multi-Hand Detection with Sound", output_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()