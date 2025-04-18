import pygame
from PIL import Image, ImageFilter

from gfx.gradient import gradient


class Spike(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)

        self.surface = surface
        self.x = x
        self.y = y
        self.rect = self.surface.get_rect(center=(self.x, self.y))


class SpikeFactory:
    def __init__(
        self,
        border_color: pygame.Color | str = "#ffffff",
        size: int = 50,
        thickness: int = 2,
        bloom_radius: int = 10
    ):
        self.size = size
        self.thickness = thickness
        self.border_color = border_color
        self.bloom_radius = bloom_radius

        self.spike_sprite = self.draw()

    @property
    def full_size(self):
        return self.size + self.thickness

    @property
    def surface_points(self) -> list[tuple[int, int]]:
        return [(0, self.size), (self.size, self.size), (self.size // 2, 0)]

    @property
    def masks(self) -> list[list[tuple[int, int]]]:
        mask_a = [(0, 0), (self.full_size // 2, 0), (0, self.full_size)]
        mask_b = [(self.full_size, 0), (self.full_size // 2, 0), (self.full_size, self.full_size)]
        return [mask_a, mask_b]

    def draw_masks(self, surface: pygame.Surface) -> None:
        for mask in self.masks:
            pygame.draw.polygon(surface, '#00000000', mask)

    def draw_gradient(self, surface: pygame.Surface) -> None:
        surface.blit(gradient(
            '#000000ff', '#00000000',
            self.full_size, self.full_size), (0, 0)
        )

    def draw_border(self, surface: pygame.Surface) -> None:
        pygame.draw.lines(surface, self.border_color, True, self.surface_points, width=self.thickness)

    def add_bloom(self, surface: pygame.Surface) -> None:
        bloom_surface = pygame.Surface((self.full_size, self.full_size), pygame.SRCALPHA)
        self.draw_border(bloom_surface)

        surf_str = pygame.image.tostring(bloom_surface, 'RGBA', False)
        surf_size = bloom_surface.get_size()
        pil_blured = (Image.frombytes("RGBA", surf_size, surf_str)
                      .filter(ImageFilter.GaussianBlur(radius=self.bloom_radius)))

        surf_pygame = pygame.image.fromstring(pil_blured.tobytes("raw"), surf_size, "RGBA")
        surface.blit(surf_pygame, (0, 0))


    def draw(self) -> pygame.Surface:
        surface = pygame.Surface((self.full_size, self.full_size), pygame.SRCALPHA)

        self.draw_gradient(surface)
        self.add_bloom(surface)

        self.draw_masks(surface)
        self.draw_border(surface)

        return surface

    def new(self, x: int, y: int):
        return Spike(x, y, self.spike_sprite)
