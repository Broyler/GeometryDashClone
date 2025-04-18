import pygame


def gradient(start_color: str | pygame.Color,
            end_color: str | pygame.Color,
            width: int,
            height: int) -> pygame.Surface:
    gradient_bitmap = pygame.Surface((2, 2), pygame.SRCALPHA)
    pygame.draw.line(gradient_bitmap, start_color, (0, 0), (1, 0))
    pygame.draw.line(gradient_bitmap, end_color, (0, 1), (1, 1))
    gradient_bitmap = pygame.transform.smoothscale(
        gradient_bitmap,
        (width, height)
    )
    return gradient_bitmap
