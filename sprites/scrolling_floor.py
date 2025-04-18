import pygame


class ScrollingFloor(pygame.sprite.Sprite):
    def __init__(self, window_surface: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)

        win_height = window_surface.get_height()
        self.height = int(win_height * 0.3)
        self.width = window_surface.get_width()
        self.color = pygame.Color("#0112c7")

        self.surface = self.draw()
        self.rect = self.surface.get_rect(top=win_height - self.height)

    def draw(self):
        surf = pygame.Surface((self.width, self.height))
        surf.fill(self.color)
        return surf
