import pygame
import random
import math
from attacks import Projectile

class Boss:
    def __init__(self, x, y, player, world):
        self.pos = pygame.Vector2(x, y)
        self.player = player
        self.world = world
        self.cooldown = 0
        self.bulletSpeed = 450
        self.playerPosHistory = [self.player.pos.copy()]
        self.shootCoolDown = 0.1
        self.selfPreVelocity = 50

    def update(self, dt):
        self.cooldown -= dt

        # вектор на игрока
        direction = self.player.pos - self.pos
        distance = direction.length()
        if distance > 0:
            direction = direction.normalize()
        angle = math.atan2(direction.y, direction.x)
        
        self._move_v1(angle, dt)

        if self.cooldown < 0:
            self._shoot_v1(distance)
            self.cooldown += self.shootCoolDown

    def _shoot_v1(self, distance):
        self.playerPosHistory = [self.player.pos.copy()] + self.playerPosHistory[0:4]
        print(f"History : {self.playerPosHistory}")
        playerVelocity = []
        for i in range(1, len(self.playerPosHistory)):
            playerVelocity.append((self.playerPosHistory[i-1] - self.playerPosHistory[i]) / self.shootCoolDown)
        print(f"Velocity : {playerVelocity}")
        playerMeanVelocity = sum(playerVelocity, pygame.Vector2(0, 0)) / len(playerVelocity)

        t = _lead_time(self.player.pos, playerMeanVelocity, self.pos, self.bulletSpeed)

        if t is None: aim = self.player.pos
        else: aim = self.player.pos + playerMeanVelocity * t

        _direction = aim - self.pos
        vel = _direction.normalize() * self.bulletSpeed
        spawn_pos = self.pos + vel.normalize() * 16

        self.world.projectiles.append(Projectile(spawn_pos, vel, radius=4, ttl=2.5))

        print(f"<V> : {playerMeanVelocity} ")
    def _move_v1(self, angle, dt):
        selfVelocity = pygame.Vector2(math.cos(angle), math.sin(angle))
        if selfVelocity.length() > 0:
            selfVelocity = selfVelocity.normalize()
        self.pos += selfVelocity * dt * self.selfPreVelocity


    def draw(self, screen, offset):
        pygame.draw.circle(screen, (255, 50, 50), self.pos - offset, 12)



def _lead_time(p, v, s, bullet_speed):
    r = p - s  # вектор от стрелка к игроку

    a = v.dot(v) - bullet_speed * bullet_speed
    b = 2.0 * r.dot(v)
    c = r.dot(r)

    # если a ~ 0, уравнение почти линейное
    if abs(a) < 1e-6:
        if abs(b) < 1e-6:
            return None
        t = -c / b
        return t if t > 0 else None

    disc = b*b - 4*a*c
    if disc < 0:
        return None

    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)

    # берём минимальное положительное время
    t = min(t for t in (t1, t2) if t > 0) if (t1 > 0 or t2 > 0) else None
    return t