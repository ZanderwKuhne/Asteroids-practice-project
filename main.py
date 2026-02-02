import pygame
import sys
import ui
import circleshape
from shot import Shot
from asteroidfield import AsteroidField
import player
from asteroid import Asteroid
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


def game_over_screen(screen, clock, font):
    show_time = 0.0
    while show_time < 3.0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        screen.fill("black")
        ui.game_over(screen, font, "GAME OVER")
        pygame.display.flip()

        dt = clock.tick(60) / 1000
        show_time += dt
    countdown = 10.0
    while countdown > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True
        countdown -= clock.tick(60) / 1000

        screen.fill("black")
        ui.game_over(screen, font, "Continue?", y_offset=-20)
        ui.game_over(screen, font, "Press Enter to try again")
        ui.game_over(screen, font, f"{int(countdown)}", y_offset=20)
        pygame.display.flip()
    return False


def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    running = True
    font = pygame.font.SysFont(None, 30)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while running:
        elapsed_time = 0.0
        score = 0
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
        while player_char.lives > 0:
            log_state()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            updatable.update(dt)

            for rock in asteroids:
                if player_char.collides_with(rock):
                    log_event("player_hit")
                    player_char.respawn()

            for rock in asteroids:
                for bullet in shots:
                    if bullet.collides_with(rock):
                        log_event("asteroid_shot")
                        score += rock.score
                        rock.split(screen)
                        bullet.kill()
            screen.fill("black")
            for drawables in drawable:
                drawables.draw(screen)
            ui.draw_lives(screen, font, player_char.lives)
            ui.draw_timer(screen, font, elapsed_time)
            ui.draw_score(screen, font, score)
            pygame.display.flip()
            dt = clock.tick(60) / 1000
            elapsed_time += dt
        running = game_over_screen(screen, clock, font)
    print("Game over!")
    sys.QUIT


if __name__ == "__main__":
    main()
