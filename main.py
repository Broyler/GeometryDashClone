import pygame

from sprites.spike import Spike, SpikeFactory
from sprites.scrolling_floor import ScrollingFloor

pygame.init()

WINDOW_SIZE = (800, 600)
# WINDOW_SIZE = (1200, 1000)

window = pygame.display.set_mode(WINDOW_SIZE)

bg = pygame.Surface(WINDOW_SIZE)
bg.fill(pygame.Color("#223aed"))

floor_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
floor = ScrollingFloor(floor_surface)

pygame.display.set_caption("Geometry Dash Clone")
is_running = True
clock = pygame.time.Clock()

spike_factory = SpikeFactory()
spikes = [
    spike_factory.new(100, int(floor.rect.y)),
    spike_factory.new(150, int(floor.rect.y))
]

while is_running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window.blit(bg, (0, 0))

    for spike in spikes:
        window.blit(spike.surface, spike.rect)

    floor_surface.fill('#00000000')
    floor_surface.blit(floor.surface, floor.rect)
    window.blit(floor_surface, (0, 0))

    pygame.display.update()
