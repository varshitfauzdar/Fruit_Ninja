import cv2
import time
from collections import deque
from hand_tracker import HandTracker
from fruit import Fruit

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

tracker = HandTracker()

fruits = []
score = 0
spawn_timer = 0

# Slash trail memory
trail_points = deque(maxlen=15)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    landmarks = tracker.get_landmarks(frame)

    # Spawn fruit every 1.5 sec (slower)
    if time.time() - spawn_timer > 1.5:
        fruits.append(Fruit(w, h))
        spawn_timer = time.time()

    # Move & draw fruits
    for fruit in fruits[:]:
        fruit.move()
        fruit.draw(frame)

        if fruit.is_off_screen(h):
            fruits.remove(fruit)

        if landmarks:
            fx, fy = landmarks[8][1], landmarks[8][2]

            # Add to trail
            trail_points.append((fx, fy))

            if fruit.is_sliced(fx, fy):
                fruits.remove(fruit)
                score += 1

    # Draw slash trail
    for i in range(1, len(trail_points)):
        thickness = int(8 * (1 - i / len(trail_points)))
        cv2.line(frame,
                 trail_points[i - 1],
                 trail_points[i],
                 (0, 255, 255),
                 thickness)

    # Score display
    cv2.putText(frame, f"Score: {score}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    cv2.imshow("AirSlash - Enhanced", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
