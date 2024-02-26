import pygame
from player import Enemy, Enemy2, Enemy3
class Chest(Enemy):
    def __init__(self, x, y):
        """ Constructor function """
        super().__init__(x, y)
        self.image = pygame.image.load("chest.png") #https://www.google.com/search?q=chest+pixel+png&sca_esv=3b24e9ecc5dcdeb0&rlz=1C1CHBF_zh-CNCA965CA965&tbm=isch&sxsrf=ACQVn08pNe3gNU5TJ-MXWX02fjXiMibYqg:1708236223990&source=lnms&sa=X&ved=2ahUKEwi03crqm7SEAxWrMVkFHVkODg0Q_AUoAXoECAEQAw&biw=1493&bih=1062&dpr=1.35#imgrc=VpPfSseIF7lY6M
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.maxhealth = 10
        self.dead_timer = 1000000
        self.currenthealth = self.maxhealth
        self.is_dead = False

    def update(self, player, walls, room):
        if self.currenthealth <= 0:
            self.image = pygame.image.load("chest_open.png") #https://www.google.com/search?q=chest+pixel+png&sca_esv=3b24e9ecc5dcdeb0&rlz=1C1CHBF_zh-CNCA965CA965&tbm=isch&sxsrf=ACQVn08pNe3gNU5TJ-MXWX02fjXiMibYqg:1708236223990&source=lnms&sa=X&ved=2ahUKEwi03crqm7SEAxWrMVkFHVkODg0Q_AUoAXoECAEQAw&biw=1493&bih=1062&dpr=1.35#imgrc=GWjZmF70TXPSdM
            self.image = pygame.transform.scale(self.image, (50, 70))
            self.is_dead = True
            self.dead_timer -= pygame.time.get_ticks()
            if self.dead_timer <= 0:
                self.kill()
                player.attack_damage += 20

class Chest2(Chest):
    def __init__(self, x, y):
        """ Constructor function """
        super().__init__(x, y)

    def update(self, player, walls, room):
        if self.currenthealth <= 0:
            self.image = pygame.image.load("chest_open.png") #https://www.google.com/search?q=chest+pixel+png&sca_esv=3b24e9ecc5dcdeb0&rlz=1C1CHBF_zh-CNCA965CA965&tbm=isch&sxsrf=ACQVn08pNe3gNU5TJ-MXWX02fjXiMibYqg:1708236223990&source=lnms&sa=X&ved=2ahUKEwi03crqm7SEAxWrMVkFHVkODg0Q_AUoAXoECAEQAw&biw=1493&bih=1062&dpr=1.35#imgrc=GWjZmF70TXPSdM
            self.image = pygame.transform.scale(self.image, (50, 70))
            self.is_dead = True
            self.dead_timer -= pygame.time.get_ticks()
            if self.dead_timer <= 0:
                self.kill()
                #spawn monster
                room.enemy_sprites.add(Enemy(640, 150))
                room.enemy_sprites.add(Enemy2(540, 150))
                room.enemy_sprites.add(Enemy2(540, 350))
                room.enemy_sprites.add(Enemy3(640, 350))

