import random
import cv2
import math

class Fruit:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Spawn from bottom
        self.x = random.randint(50, width - 50)
        self.y = height

        self.radius = random.randint(20, 30)

        # Bright random color
        self.color = (
            random.randint(80, 255),
            random.randint(80, 255),
            random.randint(80, 255)
        )

        # Gravity strength
        self.gravity = 0.6

        # Target height between 75% and 125% of screen height
        height_percent = random.uniform(0.75, 1.25)
        target_height = height * height_percent

        # Physics formula:
        # v^2 = 2 * g * h
        # Calculate required upward velocity
        self.vel_y = -math.sqrt(2 * self.gravity * target_height)

    def move(self):
        # Apply gravity
        self.vel_y += self.gravity
        self.y += self.vel_y

    def draw(self, frame):
        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            self.radius,
            self.color,
            -1
        )

    def is_off_screen(self, height):
        return self.y > height + 50

    def is_sliced(self, fx, fy):
        return (fx - self.x) ** 2 + (fy - self.y) ** 2 <= self.radius ** 2
