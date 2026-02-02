import pygame
from asteroid import Asteroid
from shot import Shot
import circleshape
from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOT_COOLDOWN,
    LINE_WIDTH,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SHOT_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Player(circleshape.CircleShape):
    def __init__(self, x, y, cooldown):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = cooldown
        self.lives = 3

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            if self.cooldown > 0:
                pass
            else:
                self.shoot()
                self.cooldown = PLAYER_SHOT_COOLDOWN
        self.cooldown -= dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        bullet = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        bullet.velocity = (
            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        )

    def respawn(self):
        self.lives -= 1
        self.position.x = SCREEN_WIDTH / 2
        self.position.y = SCREEN_HEIGHT / 2
        self.cooldown = 0
        self.rotation = 0
