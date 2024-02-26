import pygame
from player import Sprite

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Room(object):
    """ Base class for all rooms. """

    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.box_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


class Room1(Room):
    """This creates all the walls in room 1"""

    def __init__(self):
        super().__init__()
        # Make the walls. (x_pos, y_pos, width, height)

        # This is a list of walls. Each is in the form [x, y, width, height]
        walls = [[0, 0, 20, 250, WHITE],
                 [0, 350, 20, 250, WHITE],
                 [780, 0, 20, 250, WHITE],
                 [780, 350, 20, 250, WHITE],
                 [20, 0, 760, 20, WHITE],
                 [20, 580, 760, 20, WHITE],
                 [390, 100, 20, 300, WHITE]
                 ]

        # Loop through the list. Create the wall, add it to the list
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

class Room2(Room):
    """This creates all the walls in room 2"""

    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, WHITE],
                 [0, 350, 20, 250, WHITE],
                 [780, 0, 20, 250, WHITE],
                 [780, 350, 20, 250, WHITE],
                 [20, 0, 250, 20, WHITE],
                 [400, 0, 400, 20, WHITE],
                 [20, 580, 760, 20, WHITE]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

class Room3(Room):
    """This creates all the walls in room 2"""

    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 700, WHITE],#left wall
                 [780, 0, 20, 700, WHITE], #right wall
                 [20, 0, 760, 20, WHITE], #top wall
                 [20, 580, 250, 20, WHITE], #bottom walls
                 [400, 580, 400, 20, WHITE]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

class Room4(Room):
    """This creates all the walls in room 2"""

    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, WHITE],
                 [0, 350, 20, 250, WHITE],#left wall
                 [780, 0, 20, 250, WHITE],
                 [780, 350, 20, 250, WHITE], #right wall
                 [20, 0, 250, 20, WHITE], # top
                 [400, 0, 400, 20, WHITE],
                 [20, 580, 250, 20, WHITE],  # bottom walls
                 [400, 580, 400, 20, WHITE]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

class Room5(Room):
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 700, WHITE],#left wall
                 [780, 0, 20, 700, WHITE], #right wall
                 [20, 0, 760, 20, WHITE], #top wall
                 [20, 580, 250, 20, WHITE], #bottom walls
                 [400, 580, 400, 20, WHITE]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Room6(Room):
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, WHITE],
                 [0, 350, 20, 250, WHITE],#left wall
                 [780, 0, 20, 700, WHITE], #right wall
                 [20, 0, 760, 20, WHITE], #top wall
                 [20, 580, 760, 20, WHITE]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

class Room7(Room):
    def __init__(self):
        super().__init__()

        walls = [[20, 0, 250, 20, RED],  # top
                 [400, 0, 400, 20, RED],
                 [0, 0, 20, 700, RED],  # left wall
                 [780, 0, 20, 700, RED],  #right wall
                 [20, 580, 760, 20, RED],
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
