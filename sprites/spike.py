import pygame

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
        size: int = 60,
        thickness: int = 2,
        bloom_radius: int = 10
    ):
        self.size = size
        self.thickness = thickness
        self.border_color = border_color
        self.bloom_radius = bloom_radius
        self.pad = 5
        self.spike_sprite = self.draw()

    @property
    def full_size(self):
        return self.size + self.thickness

    @property
    def surface_points(self) -> list[tuple[int, int]]:
        return [(self.pad, self.size-self.pad),
                (self.size - self.pad, self.size - self.pad),
                (self.size // 2, self.pad)]

    @property
    def masks(self) -> tuple:
        k = 4
        mask_a = [(0, 0), (self.full_size // 2 + k, 0), (0, self.full_size)]
        mask_b = [(self.full_size, 0), (self.full_size // 2 - k, 0), (self.full_size, self.full_size)]
        return mask_a, mask_b

    @property
    def blur_masks(self) -> tuple:
        k = 5
        mask_a = [(0, 0), (self.full_size // 2 - k, 0), (-k, self.full_size)]
        mask_b = [(self.full_size, 0), (self.full_size // 2 + k, 0), (self.full_size + k, self.full_size)]
        return mask_a, mask_b

    @staticmethod
    def draw_masks(surface: pygame.Surface, masks: tuple) -> None:
        for mask in masks:
            pygame.draw.polygon(surface, '#00000000', mask)

    def draw_gradient(self, surface: pygame.Surface) -> None:
        surface.blit(gradient(
            '#000000ff', '#00000000',
            self.full_size, self.full_size), (0, 0)
        )

    def draw_border(self, surface: pygame.Surface, thickness: int | None = None) -> None:
        if thickness is None:
            thickness = self.thickness

        pygame.draw.lines(surface, self.border_color, True, self.surface_points, width=thickness)

    def add_bloom(self, surface: pygame.Surface) -> None:
        k = 1
        t = 3
        r = 2

        bloom_surface = pygame.Surface((self.full_size, self.full_size), pygame.SRCALPHA, 32)
        bloom_surface.fill('#ffffff00')
        self.draw_border(bloom_surface, thickness=t)
        bloom_surface = pygame.transform.gaussian_blur(bloom_surface, r, True)
        bloom_surface = pygame.transform.smoothscale(bloom_surface, (self.full_size * k, self.full_size * k))

        offset = -self.full_size * abs(k - 1) / 2

        surface.blit(bloom_surface, (offset, offset))

    def draw(self) -> pygame.Surface:
        surface = pygame.Surface((self.full_size, self.full_size), pygame.SRCALPHA)

        self.draw_gradient(surface)
        SpikeFactory.draw_masks(surface, self.masks)
        self.draw_border(surface)

        self.add_bloom(surface)
        SpikeFactory.draw_masks(surface, self.blur_masks)

        return surface

    def new(self, x: int, y: int):
        return Spike(x, y, self.spike_sprite)

    def right_of(self, spike: Spike) -> Spike:
        x = int(spike.x + spike.rect.width - 2 * self.pad)
        y = spike.x
        return Spike(x, y, self.spike_sprite)
