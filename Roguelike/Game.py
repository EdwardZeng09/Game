import pygame
from map import Room1, Room2, Room3, Room4, Room5, Room6, Room7
from player import Player, Enemy, Enemy2, Enemy3
from chest import  Chest, Chest2
from healing_fountain import Fountain
from boss import Boss

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

def main():
    """ Main Program """

    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([800, 600])

    # Set the title of the window
    pygame.display.set_caption('Maze Runner')

    # Create the player paddle object
    player = Player(20, 270)

    font = pygame.font.Font(None, 74)
    rooms = []

    room = Room1()
    room1= Room2()
    room2 = Room3()
    room4 = Room4()
    room5 = Room5()
    room6 = Room6()
    room7 = Room7()
    rooms.append(room)
    rooms.append(room1)
    rooms.append(room2)
    rooms.append(room4)
    rooms.append(room5)
    rooms.append(room6)
    rooms.append(room7)
    room2.enemy_sprites.add(Chest(355, 120))
    room.enemy_sprites.add(Enemy(500,70))
    room7.enemy_sprites.add(Boss(400, 300))
    room4.enemy_sprites.add(Enemy3(600, 70))
    room4.enemy_sprites.add(Enemy2(675, 40))
    room4.enemy_sprites.add(Enemy2(675, 400))
    room5.enemy_sprites.add(Fountain(355, 120))
    room6.enemy_sprites.add(Chest2(640, 250))
    for i in room6.enemy_sprites:
        chest_monster = i
    for i in room7.enemy_sprites:
        boss = i
    current_room_no = 0
    current_room = rooms[current_room_no]

    clock = pygame.time.Clock()
    done = False
    while not done:

        # --- Event Processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        player.update(current_room.wall_list, current_room.enemy_sprites, current_room)

        # --- Game Logic ---
        enemies_alive = any(not enemy.is_dead for enemy in current_room.enemy_sprites) #check if all enemy died
        if not enemies_alive or current_room_no == 4 or current_room_no == 2 or (current_room_no == 5 and not chest_monster.is_dead):
            if current_room_no == 5 and chest_monster.is_dead and (enemy.is_dead for enemy in current_room.enemy_sprites) and (player.attack_damage == 30 or player.attack_damage == 50):
                player.attack_damage += 10  # give player buff
                player.maxhealth += 50
                #left door
            if player.rect.x < -15:
                if current_room_no == 0:
                    current_room_no = 2
                elif current_room_no == 1:
                    current_room_no = 0
                elif current_room_no == 3:
                    current_room_no = 1
                elif current_room_no == 5:
                    current_room_no = 3
                current_room = rooms[current_room_no]
                player.rect.x = 740
                player.rect.y = 250
            #right door
            if player.rect.x > 801:
                if current_room_no == 0:
                    current_room_no = 1
                elif current_room_no == 1:
                    current_room_no = 3
                elif current_room_no == 3:
                    current_room_no = 5
                current_room = rooms[current_room_no]
                player.rect.x = 0
            #up door
            if player.rect.y < -30:
                if current_room_no == 1:
                    current_room_no = 2
                elif current_room_no == 3:
                    current_room_no = 4

                current_room = rooms[current_room_no]
                player.rect.x = 310
                player.rect.y = 510

            #bottom door
            if player.rect.y > 550:
                if current_room_no == 2:
                    current_room_no = 1
                elif current_room_no == 3:
                    current_room_no = 6
                elif current_room_no == 4:
                    current_room_no = 3
                current_room = rooms[current_room_no]
                player.rect.x = 310
                player.rect.y = -30
        else: #prevent player go to next room
            if current_room_no == 0:
                if player.rect.x > 800:
                    player.rect.x = 740
                    player.rect.y = 250
            elif current_room_no == 3:
                if player.rect.x > 800:
                    player.rect.x = 740
                    player.rect.y = 250
                elif player.rect.x < -15:
                    player.rect.x = 5
                    player.rect.y = 250
                elif player.rect.y < -30:
                    player.rect.x = 305
                    player.rect.y = -20
                elif player.rect.y > 550:
                    player.rect.x = 305
                    player.rect.y = 535
            elif current_room_no == 5:
                if player.rect.x < -15:
                    player.rect.x = 5
                    player.rect.y = 250
            elif current_room_no == 6:
                if player.rect.y < -30:
                    player.rect.x = 305
                    player.rect.y = -20
        # --- Drawing ---
        screen.fill(BLACK)
        player.draw(screen)
        current_room.wall_list.draw(screen)
        current_room.box_list.draw(screen)
        current_room.enemy_sprites.draw(screen)
        for i in current_room.enemy_sprites:
            i.draw_health_bar(screen)
            i.update(player, current_room.wall_list, current_room)
            if not isinstance(i, Chest):
                i.bullets.draw(screen)
                i.bullets.update(current_room.wall_list, player, current_room)
        player.draw_health_bar(screen)
        pygame.display.flip()
        if boss.is_dead:
            text = font.render("You Win!", True, (255, 0, 0))
            screen.blit(text, (250, 250))
            pygame.display.flip()
            pygame.time.wait(5000)  # Pause with "Game Over" visible
            done = True
        elif player.is_dead:
            text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(text, (250, 250))
            pygame.display.flip()
            pygame.time.wait(5000)  # Pause with "Game Over" visible
            done = True
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()