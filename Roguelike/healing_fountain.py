import pygame
from player import Enemy

class Fountain(Enemy):
    def __init__(self, x, y):
        """ Constructor function """
        super().__init__(x, y)
        self.image = pygame.image.load("healing.png")
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.maxhealth = 10
        self.currenthealth = self.maxhealth
        self.is_dead = False

    def update(self, player, walls, room):
        if self.rect.colliderect(player.rect):
            player.current_health = player.maxhealth
    def draw_health_bar(self, screen):
        return