import pygame

class Projectile:
    def __init__(self, pos, vel, radius=4, ttl=2.5, dmg = 10):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.radius = radius
        self.ttl = ttl  # time to live (сек)
        self.dmg = dmg
        self.alive = True

    def update(self, dt):
        self.pos += self.vel * dt
        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False

    def draw(self, screen, offset):
        pygame.draw.circle(screen, (255, 230, 80), self.pos - offset, self.radius)

    def killyour(self):
        self.alive = False