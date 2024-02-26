import pygame
import math
from player import Enemy, Bullet
import random
class Boss(Enemy):
    def __init__(self, x, y):
        """ Constructor function """
        super().__init__(x, y)
        size = (400, 400)
        self.image = pygame.transform.scale(pygame.image.load("Idle1.png"), size)#https://craftpix.net/freebies/free-rpg-monster-sprites-pixel-art/
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.dead_image = pygame.transform.scale(pygame.image.load("Death5.png"), size)
        self.moving_frames = [pygame.transform.scale(pygame.image.load(f"Walk{i}.png"), size) for i in
                             range(2, 6)]
        self.attack_frames = [pygame.transform.scale(pygame.image.load(f"d_Attack{i}.png"), size) for i in range(1, 5)]
        self.skill_timer = 0
        self.skill_interval = 100
        self.maxhealth = 500
        self.currenthealth = self.maxhealth
    def draw_health_bar(self, screen):
        bar_length = 50
        bar_height = 5
        bar_color = (255, 0, 0)
        background_color = (255, 255, 255)

        health_ratio = self.currenthealth / self.maxhealth
        current_bar_length = bar_length * health_ratio

        bar_x = self.rect.x + (self.rect.width / 2) - (bar_length / 2)
        bar_y = self.rect.y - bar_height

        pygame.draw.rect(screen, background_color, (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, current_bar_length, bar_height))

    def skill3(self, player):
        now = pygame.time.get_ticks()
        distance = math.sqrt((player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2)
        if now - self.last_bullet_time > self.bullet_cooldown:  # If player is in the range
            self.is_attacking = True
            self.last_bullet_time = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, player.rect.center, self.attack)
            self.bullets.add(bullet)
        else:
            self.is_attacking = False

    def skill1(self):
        self.is_attacking = True
        num_bullets = 10
        spread_angle = 90
        bullet_speed = 3
        for i in range(num_bullets):
            angle = (360 / num_bullets) * i
            angle_rad = math.radians(angle)
            dx = bullet_speed * math.cos(angle_rad)
            dy = bullet_speed * math.sin(angle_rad)

            b = Bullet1(self.rect.centerx, self.rect.centery, dx, dy)
            self.bullets.add(b)

    def skill2(self):
        self.is_attacking = True
        num_bullets = 10
        speed = 3
        curve_strength = 0.2
        for i in range(num_bullets):
            angle = (360 / num_bullets) * i
            angle_rad = math.radians(angle)
            dx = speed * math.cos(angle_rad)
            dy = speed * math.sin(angle_rad)

            ddx = curve_strength * math.cos(angle_rad + math.pi / 2)
            ddy = curve_strength * math.sin(angle_rad + math.pi / 2)

            bullet = Bullet2(self.rect.centerx, self.rect.bottom, 0, speed, ddx, 0)
            self.bullets.add(bullet)

    def update(self, player, walls, room):
        if not self.is_attacking:
            self.random_move(walls)
            self.animate_move()
        self.skill_timer += 1
        if self.skill_timer >= self.skill_interval:
            self.use_random_skill(player)
            self.skill_timer = 0
        else:
            self.is_attacking = False
        if self.is_attacking:
            self.animate_attack()
        if self.currenthealth <= 0:
            self.image = self.dead_image
            self.is_dead = True
            self.dead_timer -= pygame.time.get_ticks()
            if self.dead_timer <= 0:
                self.kill()


    def use_random_skill(self, player):
        # Randomly choose a skill
        skill_choice = random.randint(1, 3)
        if skill_choice == 1:
            self.skill1()
        elif skill_choice == 2:
            self.skill2()
        else:
            for i in range(3):
                self.skill3(player)
class Bullet1(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy
        self.attack = 40

    def update(self, walls, player, room):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()  # Remove the bullet
        # Check for collision with the player
        if pygame.sprite.spritecollideany(self, [player]) and self.get_hited == False:
            player.current_health -= self.attack
            self.get_hited = True
            self.kill()
        elif not pygame.sprite.spritecollideany(self, [player]):
            self.get_hited = False

class Bullet2(Bullet1):
    def __init__(self, x, y, dx, dy, ddx, ddy):
        super().__init__(x, y, dx, dy)
        self.ddx = ddx
        self.ddy = ddy

    def update(self, walls, player, room):
        self.dx += self.ddx
        self.dy += self.ddy
        self.rect.x += self.dx
        self.rect.y += self.dy
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()  # Remove the bullet
        # Check for collision with the player
        if pygame.sprite.spritecollideany(self, [player]) and self.get_hited == False:
            player.current_health -= self.attack
            self.get_hited = True
            self.kill()
        elif not pygame.sprite.spritecollideany(self, [player]):
            self.get_hited = False