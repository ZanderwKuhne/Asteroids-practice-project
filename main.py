import pygame
import sys
import circleshape
from shot import Shot
from asteroidfield import AsteroidField
import player
from asteroid import Asteroid
from logger import log_state, log_event
from constants import PLAYER_SHOT_COOLDOWN, SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Actual screen size:", screen.get_size())
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Asteroid.containers = (asteroids, updatable, drawable)
    player.Player.containers = (updatable, drawable)
    asteroid_field = AsteroidField()
    player_char = player.Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 0)
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)

        for rock in asteroids:
            if player_char.collides_with(rock):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        for rock in asteroids:
            for bullet in shots:
                if bullet.collides_with(rock):
                    log_event("asteroid_shot")
                    rock.split(screen)
                    bullet.kill()
        for drawables in drawable:
            drawables.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
