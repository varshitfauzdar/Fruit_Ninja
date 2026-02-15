import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

class HandTracker:
    def __init__(self):
        base_options = python.BaseOptions(
            model_asset_path="C:/Users/varsh/OneDrive/Desktop/ai/Fruit_Ninja/hand_landmarker.task"
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

    def get_landmarks(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        timestamp = int(time.time() * 1000)
        result = self.detector.detect_for_video(mp_image, timestamp)

        landmarks = []

        if result.hand_landmarks:
            h, w, _ = frame.shape
            hand_landmarks = result.hand_landmarks[0]

            for idx, lm in enumerate(hand_landmarks):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((idx, cx, cy))

        return landmarks
