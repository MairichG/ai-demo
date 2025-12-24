import pygame

class Player:
    def __init__(self, x, y):
        self.x0 = x
        self.y0 = y
        self.pos = pygame.Vector2(x, y)
        self.radius = 8
        self.hp = 100

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.v = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )
        if self.v.length() > 0:
            self.v = self.v.normalize()
        self.pos += self.v * 200 * dt

    def hit(self, dmg):
        self.hp -= dmg
        print(f"HP: {self.hp}")
        if self.hp <= 0:
            self.die()

    def die(self):
        print("YOU DIED")
        self.hp = 100
        self.pos = pygame.Vector2(self.x0, self.y0)

    def draw(self, screen, offset):
        
        pygame.draw.circle(screen, (0, 200, 255), self.pos - offset, 8)