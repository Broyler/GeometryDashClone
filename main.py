import pygame

from sprites.spike import Spike, SpikeFactory

pygame.init()

WINDOW_SIZE = (800, 600)
window = pygame.display.set_mode(WINDOW_SIZE)

bg = pygame.Surface(WINDOW_SIZE)
bg.fill(pygame.Color("#3244a8"))

pygame.display.set_caption("Geometry Dash Clone")
is_running = True

spike_factory = SpikeFactory()
spike = spike_factory.new(100, 100)

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window.blit(bg, (0, 0))
    window.blit(spike.surface, spike.rect)
    pygame.display.update()

