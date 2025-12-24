from player import Player
from boss import Boss

import pygame
import math

class World:
    def __init__(self):
        self.player = Player(0, 200)
        self.projectiles = []            # <-- ВОТ ОНО
        self.boss = Boss(0, 0, self.player, self)

        self.arenaCenter = pygame.Vector2(0, 0)
        self.arendaRadius = 1000
        self.outsideDPS = 20

        self.camera = pygame.Vector2(0, 0)

    def update(self, dt):
        self.player.update(dt)
        self.boss.update(dt)

        # обновление снарядов
        for p in self.projectiles:
            p.update(dt)

            dist = (p.pos - self.player.pos).length()
            if dist < p.radius + self.player.radius:
                self.player.hit(p.dmg)
                p.killyour()

        arenaDist = (self.player.pos - self.arenaCenter).length()
        if arenaDist > self.arendaRadius:
            self.player.hit(self.outsideDPS * dt)
        # удаление “мертвых” (ttl вышел)
        self.projectiles = [p for p in self.projectiles if p.alive]

        self.update_camera(dt)

    def draw(self, screen):
        screen.fill((20, 20, 20))
        offset = self.camera

        draw_grid_background(screen, self.camera, spacing=120, dot_radius=2, parallax=0.15)
        draw_grid_background(screen, self.camera, spacing=60,  dot_radius=1, parallax=0.35)
        draw_grid_background(screen, self.camera, spacing=20,  dot_radius=1, parallax=1)

        centerScreen = self.arenaCenter - offset
        pygame.draw.circle(screen, (180, 120, 255), centerScreen, self.arendaRadius, 3)

        self.player.draw(screen, offset)
        self.boss.draw(screen, offset)

        for p in self.projectiles:
            p.draw(screen, offset)
        
        self.draw_hp(screen)
    
    def draw_hp(self, screen):
        # позиция и размеры (снизу слева)
        margin = 16
        bar_w, bar_h = 220, 18
        x = margin
        y = screen.get_height() - margin - bar_h

        # значения HP
        hp = max(0, self.player.hp)
        hp_max = 100  # если хочешь — потом сделаем self.player.max_hp
        ratio = hp / hp_max

        # фон бара
        pygame.draw.rect(screen, (40, 40, 40), (x, y, bar_w, bar_h), border_radius=6)

        # заполнение
        fill_w = int(bar_w * ratio)
        pygame.draw.rect(screen, (0, 200, 100), (x, y, fill_w, bar_h), border_radius=6)

        # обводка
        pygame.draw.rect(screen, (220, 220, 220), (x, y, bar_w, bar_h), 2, border_radius=6)

        # текст
        if not hasattr(self, "_font"):
            self._font = pygame.font.SysFont("consolas", 18)

        text = self._font.render(f"HP {int(hp)}/{hp_max}", True, (240, 240, 240))
        screen.blit(text, (x, y - 22))


    def update_camera(self, dt):
        screen_w, screen_h = 800, 600
        target = self.player.pos - pygame.Vector2(screen_w / 2, screen_h / 2)

        smooth = 1
        alpha = 1 - math.exp(-smooth * dt)
        self.camera += (target - self.camera) * alpha


def draw_grid_background(screen, camera, spacing=80, dot_radius=2, parallax=0.3):
    w, h = screen.get_size()

    # параллакс-смещение
    offset = camera * parallax

    # стартовые координаты (чтобы сетка была бесконечной)
    start_x = -int(offset.x % spacing)
    start_y = -int(offset.y % spacing)

    color = (60, 70, 70)

    for x in range(start_x, w + spacing, spacing):
        for y in range(start_y, h + spacing, spacing):
            pygame.draw.circle(screen, color, (x, y), dot_radius)