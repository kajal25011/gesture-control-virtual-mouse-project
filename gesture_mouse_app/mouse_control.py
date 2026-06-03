import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ---------------- VOLUME SETUP ----------------
device = AudioUtilities.GetSpeakers()
interface = device.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol = volume.GetVolumeRange()[:2]

# ---------------- MEDIAPIPE SETUP ----------------
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

dragging = False  # Drag state

# ---------------- FINGER STATE FUNCTION ----------------
def fingers_up(hand):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(1 if hand.landmark[4].x < hand.landmark[3].x else 0)

    # Other fingers
    for i in range(1, 5):
        fingers.append(
            1 if hand.landmark[tips[i]].y < hand.landmark[tips[i] - 2].y else 0
        )
    return fingers

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm = hand_landmarks.landmark
                fingers = fingers_up(hand_landmarks)

                x = int(lm[8].x * screen_w)
                y = int(lm[8].y * screen_h)

                # ---------------- CURSOR MOVE ----------------
                if fingers == [0, 1, 0, 0, 0]:
                    pyautogui.moveTo(x, y, duration=0.05)

                # ---------------- LEFT CLICK ----------------
                elif fingers == [0, 1, 1, 0, 0]:
                    pyautogui.click()
                    pyautogui.sleep(0.3)

                # ---------------- RIGHT CLICK ----------------
                elif fingers == [1, 0, 0, 0, 1]:
                    pyautogui.rightClick()
                    pyautogui.sleep(0.3)

                # ---------------- DOUBLE CLICK ----------------
                elif fingers == [0, 1, 1, 1, 0]:
                    pyautogui.doubleClick()
                    pyautogui.sleep(0.4)

                # ---------------- SCROLL ----------------
                elif fingers == [0, 0, 1, 1, 1]:
                    pyautogui.scroll(40)
                elif fingers == [0, 1, 0, 1, 0]:
                    pyautogui.scroll(-40)

                # ---------------- DRAG & DROP ----------------
                if fingers == [1, 1, 0, 0, 0]:
                    dist = np.hypot(
                        lm[4].x - lm[8].x,
                        lm[4].y - lm[8].y
                    )

                    # Start drag (fingers close)
                    if dist < 0.03 and not dragging:
                        pyautogui.mouseDown()
                        dragging = True

                    # Drag move
                    if dragging:
                        pyautogui.moveTo(x, y, duration=0.03)

                    # Brightness control (fingers apart)
                    if dist > 0.05:
                        bright = np.interp(dist, [0.05, 0.12], [0, 100])
                        sbc.set_brightness(int(bright))

                else:
                    if dragging:
                        pyautogui.mouseUp()
                        dragging = False

                # ---------------- VOLUME CONTROL ----------------
                if fingers == [1, 1, 1, 0, 0]:
                    dist = np.hypot(
                        lm[4].x - lm[8].x,
                        lm[4].y - lm[8].y
                    )
                    vol = np.interp(dist, [0.03, 0.12], [min_vol, max_vol])
                    volume.SetMasterVolumeLevel(vol, None)

                # Draw landmarks
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Gesture Virtual Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
