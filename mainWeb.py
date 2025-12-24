import pygame
from world import World
import asyncio

async def main():
    pygame.init()   
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    world = World()

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.update(dt)
        world.draw(screen)

        pygame.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())
