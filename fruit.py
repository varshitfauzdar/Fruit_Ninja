import random
import cv2

class Fruit:
    def __init__(self, width, height):
        self.x = random.randint(50, width - 50)
        self.y = height

        self.radius = random.randint(20, 30)

        self.color = (
            random.randint(80, 255),
            random.randint(80, 255),
            random.randint(80, 255)
        )

        # Physics
        self.vel_y = random.uniform(-15, -10)  # upward initial velocity
        self.gravity = 0.6
        self.alive = True

    def move(self):
        self.vel_y += self.gravity
        self.y += self.vel_y

    def draw(self, frame):
        cv2.circle(frame, (int(self.x), int(self.y)),
                   self.radius, self.color, -1)

    def is_off_screen(self, height):
        return self.y > height + 50

    def is_sliced(self, fx, fy):
        return (fx - self.x)**2 + (fy - self.y)**2 <= self.radius**2
