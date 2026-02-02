import constants


def draw_lives(screen, font, lives):
    text = font.render(f"lives: {lives}", True, (255, 255, 255))
    rect = text.get_rect(topright=(constants.SCREEN_WIDTH - 10, 10))
    screen.blit(text, rect)


def draw_timer(screen, font, elapsed_time):
    seconds_int = int(elapsed_time)
    text = font.render(f"Time: {seconds_int}", True, (255, 255, 255))
    rect = text.get_rect(topleft=(10, 10))
    screen.blit(text, rect)


def draw_score(screen, font, score):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    rect = text.get_rect(midtop=(constants.SCREEN_WIDTH // 2, 10))
    screen.blit(text, rect)


def game_over(screen, font, text, y_offset=0):
    surface = font.render(text, True, (255, 255, 255))
    rect = surface.get_rect(
        center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 + y_offset)
    )
    screen.blit(surface, rect)
