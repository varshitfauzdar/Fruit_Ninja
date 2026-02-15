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
trail_points = deque(maxlen=20)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    landmarks = tracker.get_landmarks(frame)

    # Spawn fruit every 1.5 seconds (slower gameplay)
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

            # Add finger position to trail
            trail_points.append((fx, fy))

            if fruit.is_sliced(fx, fy):
                fruits.remove(fruit)
                score += 1

    # Draw slash trail safely
    if len(trail_points) > 1:
        for i in range(1, len(trail_points)):
            pt1 = trail_points[i - 1]
            pt2 = trail_points[i]

            if pt1 is None or pt2 is None:
                continue

            thickness = int(6 * (1 - i / len(trail_points)))
            if thickness < 1:
                thickness = 1

            cv2.line(frame, pt1, pt2, (0, 255, 255), thickness)

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
