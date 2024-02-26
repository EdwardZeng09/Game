import pygame
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player(Sprite):
    """ This class represents the bar at the bottom that the
    player controls """

    # Set speed vector
    change_x = 0
    change_y = 0

    def __init__(self, x, y):
        """ Constructor function """
        super().__init__("p1.png", x, y) #https://craftpix.net/freebies/free-3-cyberpunk-characters-pixel-art/
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.facing_left = False
        self.facing_down = False
        self.facing_top = False
        self.maxhealth = 100
        self.rect = self.image.get_rect()
        self.stand_image = self.image
        self.current_health = self.maxhealth
        self.rect.y = y
        self.rect.x = x
        self.attack_index = 0
        self.is_dead = False
        self.attack_delay = 8
        self.attack_timer = 0
        self.is_attacking = False
        self.attack_cycle = [pygame.transform.scale(pygame.image.load(f"attack{i}.png"), (50, 70)) for i in range(1,6)]
        self.attack_cycle.append(self.image)
        self.attack_damage = 30
        self.animation_index = 0
        self.attack_rect = 0
        self.attack_end = False
        self.walk_cycle = []
        self.get_hited = False
        self.dead_image = pygame.transform.scale(pygame.image.load("playerdead.png"), (50, 70))
        self.walk_cycle.append(pygame.transform.scale(pygame.image.load("p1_walk01.png"), (50, 70)))
        self.walk_cycle.append(pygame.transform.scale(pygame.image.load("p1_walk02.png"), (50, 70)))
        self.walk_cycle.append(pygame.transform.scale(pygame.image.load("p1_walk03.png"), (50, 70)))
        self.walk_cycle.append(pygame.transform.scale(pygame.image.load("p1_walk04.png"), (50, 70)))
        self.walk_cycle.append(pygame.transform.scale(pygame.image.load("p1_walk05.png"), (50, 70)))
        self.walk_cycle.append(pygame.transform.scale(pygame.image.load("p1_walk06.png"), (50, 70)))


    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def draw_health_bar(self, screen):
        bar_length = 50
        bar_height = 5
        bar_color = (255, 0, 0)
        background_color = (255, 255, 255)

        health_ratio = self.current_health / self.maxhealth
        current_bar_length = bar_length * health_ratio

        bar_x = self.rect.x + (self.rect.width / 2) - (bar_length / 2)
        bar_y = self.rect.y - bar_height - 10

        pygame.draw.rect(screen, background_color, (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, current_bar_length, bar_height))

        font = pygame.font.SysFont(None, 24)  # Choose your font and size
        attack_damage_text = font.render(f"Attack: {self.attack_damage}", True, (255, 255, 255))
        # Position the text above the player's head
        screen.blit(attack_damage_text, (self.rect.x, self.rect.y - 50))

    def update(self, walls, enemys, room):
        self.change_x = 0
        self.change_y = 0
        key = pygame.key.get_pressed()
        if self.is_dead:
            return
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.facing_top = False
            self.facing_down = False
            self.walk_animation()
            self.changespeed(-5, 0)
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.facing_top = False
            self.facing_down = False
            self.walk_animation()
            self.changespeed(5, 0)
        elif key[pygame.K_UP]:
            self.walk_animation()
            self.facing_top = True
            self.facing_down = False
            self.changespeed(0, -5)
        elif key[pygame.K_DOWN]:
            self.walk_animation()
            self.facing_top = False
            self.facing_down = True
            self.changespeed(0, 5)
        else:
            if self.facing_left:
                self.image = pygame.transform.flip(self.stand_image, True, False)
            else:
                self.image = self.stand_image

        if key[pygame.K_1]:
            self.attack()

        if self.is_attacking:
            if self.attack_timer > 0:
                self.attack_timer -= 1
            else:
                self.attack_index += 1  # Move to the next frame
                if self.attack_index >= len(self.attack_cycle):
                    self.attack_index = 0  # Reset to the first frame
                    self.is_attacking = False  # End the attack animation
                    for enemy in enemys:
                        enemy.hited_by = False
                else:
                    self.image = self.attack_cycle[self.attack_index]
                    self.attack_timer = self.attack_delay
        if self.is_attacking:
            if self.facing_left:
                attack_rect = pygame.Rect(self.rect.left - 10, self.rect.top, 10, self.rect.height)
            elif self.facing_top:
                attack_rect = pygame.Rect(self.rect.left, self.rect.top - 10, self.rect.width, 10)
            elif self.facing_down:
                attack_rect = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 10)
            else:
                attack_rect = pygame.Rect(self.rect.right, self.rect.top, 10, self.rect.height)
            for enemy in enemys:
                if attack_rect.colliderect(enemy.rect):
                    if enemy.hited_by == False:
                        enemy.currenthealth -= self.attack_damage
                        enemy.hited_by = True
        if self.current_health <= 0:
            self.is_dead = True
            self.image = self.dead_image
            self.change_x = 0
            self.change_y = 0
        self.move(walls)
    def attack(self):
        """ deal damage """
        self.is_attacking = True
        self.attack_timer = self.attack_delay

    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    def move(self, walls):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

class Enemy(Sprite):
    def __init__(self, startx, starty):
        super().__init__("enemy1.png", startx, starty)
        self.maxhealth = 100
        self.currenthealth = self.maxhealth
        self.rect.y = starty
        self.rect.x = startx
        self.hited_by = False
        self.dead_timer = 500000
        self.is_dead = False #check if enemy died
        self.move_timer = 0
        self.bullet_cooldown = 2000
        self.last_bullet_time = pygame.time.get_ticks()
        self.move_direction = pygame.math.Vector2(0, 0)
        self.dead_image = pygame.image.load("enemy_dead.png")
        self.bullets = pygame.sprite.Group()
        self.speed = 2
        self.stand = self.image
        self.attack = 20
        self.animation_index = 0
        self.attack_index = 0
        self.is_attacking = False
        self.is_moving = False
        self.attack_delay = 8
        self.attack_timer = 0
        self.moving_frames = [pygame.image.load(f"enemy_w{i}.png") for i in range(1,8)]
        self.attack_frames = [pygame.image.load(f"enemy_a{i}.png") for i in range(1,10)]
        self.attack_frames.append(self.image)
        self.moving_left = False
    def draw_health_bar(self, screen):
        bar_length = 50
        bar_height = 5
        bar_color = (255, 0, 0)
        background_color = (255, 255, 255)

        health_ratio = self.currenthealth / self.maxhealth
        current_bar_length = bar_length * health_ratio

        bar_x = self.rect.x + (self.rect.width / 2) - (bar_length / 2)
        bar_y = self.rect.y - bar_height - 10

        pygame.draw.rect(screen, background_color, (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, current_bar_length, bar_height))

    def update(self, player, walls, room):
        if not self.is_attacking:
            self.random_move(walls)
        self.fire_bullet(player)
        if self.is_moving:
            self.animate_move()
        elif self.is_attacking:
            self.image = self.stand
            self.animate_attack()
        if self.currenthealth <= 0:
            self.image = self.dead_image
            self.is_dead = True
            self.dead_timer -= pygame.time.get_ticks()
            if self.dead_timer <= 0:
                self.kill()

    def animate_move(self):
        # Cycle through moving frames
        moving_left = self.move_direction.x < 0
        self.moving_left = moving_left
        # Cycle through moving frames
        frame = self.moving_frames[self.animation_index]
        if moving_left:
            # Flip the frame if moving left
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

        self.animation_index = (self.animation_index + 1) % len(self.moving_frames)

    def animate_attack(self):
        # Cycle through attack frames
        if self.is_attacking:
            self.attack_index += 1  # Move to the next frame
            if self.attack_index >= len(self.attack_frames):
                self.attack_index = 0  # Reset to the first frame
                self.is_attacking = False  # End the attack animation
            else:
                self.image = self.attack_frames[self.attack_index]

    def fire_bullet(self, player):
        now = pygame.time.get_ticks()
        distance = math.sqrt((player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2)
        if distance < 200 and now - self.last_bullet_time > self.bullet_cooldown:  # If player is in the range
            self.is_attacking = True
            self.last_bullet_time = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, player.rect.center, self.attack)
            self.bullets.add(bullet)
        else:
            self.is_attacking = False
    def random_move(self, walls):
        self.is_moving = True
        if self.move_timer <= 0:
            # Set a new random direction
            self.move_direction = pygame.math.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
            self.move_timer = random.randint(30, 100)  # Reset timer
        else:
            self.move_timer -= 1

        # Save the current position before moving
        original_position = self.rect.copy()

        # Move
        self.rect.x += self.move_direction.x * self.speed
        self.rect.y += self.move_direction.y * self.speed

        # Check for collision with any wall
        if pygame.sprite.spritecollideany(self, walls):
            # If collided, move back to the original position
            self.rect = original_position
            # Reverse direction
            self.move_direction *= -1


class Enemy2(Enemy):
    """
    unmoveable enemy
    """
    def __init__(self, startx, starty):
        super().__init__(startx, starty)
        self.bullet_cooldown = 1500

    def update(self, player, walls, room):
        self.fire_bullet(player)
        if self.is_attacking:
            self.animate_attack()
        if self.currenthealth <= 0:
            self.image = self.dead_image
            self.is_dead = True
            self.dead_timer -= pygame.time.get_ticks()
            if self.dead_timer <= 0:
                self.kill()
    def animate_attack(self):
        # Cycle through attack frames
        self.attack_index += 1  # Move to the next frame
        if self.attack_index >= len(self.attack_frames):
            self.attack_index = 0  # Reset to the first frame
            self.is_attacking = False  # End the attack animation
        else:
            self.image = self.attack_frames[self.attack_index]
            self.image = pygame.transform.flip(self.image, True, False)

    def fire_bullet(self, player):
        """all range attack"""
        now = pygame.time.get_ticks()
        if now - self.last_bullet_time > self.bullet_cooldown:  # If player is in the range
            self.is_attacking = True
            self.last_bullet_time = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, player.rect.center, self.attack)
            self.bullets.add(bullet)

class Enemy3(Enemy):
    def __init__(self, startx, starty):
        super().__init__(startx, starty)
        self.image = pygame.image.load("enemy3.png")
        self.attack_range = 50
        self.last_attack_time = pygame.time.get_ticks()
        self.moving_frames = [pygame.image.load(f"enemy3_w{i}.png") for i in range(1,8)]
        self.attack_frames = [pygame.image.load(f"enemy3_a{i}.png") for i in range(1,7)]
        self.stand = pygame.image.load("enemy3.png")
        self.dead_image =  pygame.image.load("enemy3_dead.png")
        self.attack_cooldown = 2000

    def update(self, player, walls, room):
        if not self.is_attacking:
            self.speed = 2
            self.random_move(walls)
            self.animate_move()
        distance = math.sqrt((player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2)
        if distance < 300:
            direction_vector = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
            if direction_vector.length() > 0:
                direction = direction_vector.normalize()
            else:
                direction = pygame.math.Vector2()
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed
            self.animate_move()
        current_time = pygame.time.get_ticks()
        if distance <= self.attack_range and current_time - self.last_attack_time >= self.attack_cooldown:
            self.image = pygame.image.load("enemy3_a4.png")
            self.attack1(player)
            self.last_attack_time = current_time
        if self.currenthealth <= 0:
            self.image = self.dead_image
            self.is_dead = True
            self.dead_timer -= pygame.time.get_ticks()
            if self.dead_timer <= 0:
                self.kill()

    def attack1(self, player):
        self.is_attacking = True
        if self.moving_left:
            attack_rect = pygame.Rect(self.rect.left - 10, self.rect.top, 10, self.rect.height)
        else:
            attack_rect = pygame.Rect(self.rect.right, self.rect.top, 10, self.rect.height)
        if attack_rect.colliderect(player.rect):
            player.current_health -= self.attack
        self.is_attacking = False

    def animate_attack(self):
        # Cycle through attack frames
        for i in self.attack_frames:
            if self.moving_left:
                self.image = i
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = i
class Bullet(pygame.sprite.Sprite):
    def __init__(self, startx, starty, pos, attack):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty]
        self.target_pos = pos
        self.speed = 3
        self.get_hited = False
        self.move_direction = (self.target_pos - pygame.math.Vector2(self.rect.center)).normalize()
        self.attack = attack

    def update(self, walls, player, room):
        self.rect.x += self.move_direction.x * self.speed
        self.rect.y += self.move_direction.y * self.speed
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()  # Remove the bullet
        # Check for collision with the player
        if pygame.sprite.spritecollideany(self, [player]) and self.get_hited == False:
            player.current_health -= self.attack
            self.get_hited = True
            self.kill()
        elif not pygame.sprite.spritecollideany(self, [player]):
            self.get_hited = False


