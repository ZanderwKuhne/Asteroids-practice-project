import circleshape
import constants
import pygame
import logger
import random


class Asteroid(circleshape.CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen, "white", self.position, self.radius, constants.LINE_WIDTH
        )

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self, screen):
        self.kill()
        if self.radius <= constants.ASTEROID_MIN_RADIUS:
            return
        else:
            logger.log_event("asteroid_split")
            angle = random.uniform(20, 50)
            new_velocity_1 = self.velocity.rotate(angle)
            new_velocity_2 = self.velocity.rotate(angle * -1)
            new_radius = self.radius - constants.ASTEROID_MIN_RADIUS
            split_rock_1 = Asteroid(self.position.x, self.position.y, new_radius)
            split_rock_2 = Asteroid(self.position.x, self.position.y, new_radius)
            split_rock_1.velocity += new_velocity_1 * 1.2
            split_rock_2.velocity += new_velocity_2 * 1.2
