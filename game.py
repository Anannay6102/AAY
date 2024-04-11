import pygame
import random

pygame.init()


class Room:
    # This class defines a room in a catacomb. Each room has a unique number and can be connected to other rooms in three directions: back, left, and right.
    def __init__(self, number, back_way=None):
        self.back_way = back_way  # The room from which this room was entered, if any.
        self.right_way = None  # Placeholder for a room that will be to the right of this room.
        self.left_way = None  # Placeholder for a room that will be to the left of this room.
        self.number = number  # A unique identifier for this room.


def insert_random(room, number, back_way=None):
    # This function inserts a new room into the catacomb structure at a random position (left or right) from the given room.
    if room is None:
        return Room(number, back_way)  # If there's no room, create a new one as the starting point.
    else:
        # Randomly decide whether to insert the new room to the left or right.
        if random.random() > 0.5:
            # If the left side is empty, insert the new room there.
            if room.left_way is None:
                room.left_way = Room(number, room)
            else:
                # If the left side is not empty, recursively call this function to insert the new room further down the left side.
                insert_random(room.left_way, number, room)
        else:
            # If the right side is empty, insert the new room there.
            if room.right_way is None:
                room.right_way = Room(number, room)
            else:
                # If the right side is not empty, recursively call this function to insert the new room further down the right side.
                insert_random(room.right_way, number, room)
        return room  # Return the updated structure of rooms.


def random_catacombs(n):
    # This function generates a catacomb with a specified number of rooms in a randomized layout.
    root = Room(0)  # The starting room of the catacomb.
    for i in range(1, n):
        insert_random(root, i)  # Insert each new room into the catacomb in a random position.
    return root  # Return the root of the catacomb structure after all rooms have been added.


class Point:  # make object point (character)
    def __init__(self, x, y, radius, speed):  # initialize attributes
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.radius = radius  # radius
        self.speed = speed  # speed


class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)


class Door:
    def __init__(self, x, y, width, height, direction):
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = direction


class Game:  # make object game ()
    def __init__(self):  # initialize all attributes (features) of game
        self.point = Point(320, 240, 8, 5)  # put point (character) in game
        self.screen = pygame.display.set_mode((640, 480))  # initialize the screen
        self.catacombs = random_catacombs(7)  # create and set up catacombs (tree) structure
        self.current_room = self.catacombs
        self.walls = [Wall(0, 160, 640, 10), Wall(0, 320, 640, 10), Wall(0, 160, 10, 170), Wall(630, 160, 10, 170)]
        self.doors = self.update_doors()

    def update_doors(self):
        doors = []
        if self.current_room.left_way:
            left_door = Door(20, 200, 20, 80, 'left')
            doors.append(left_door)
        if self.current_room.right_way:
            right_door = Door(600, 200, 20, 80, 'right')
            doors.append(right_door)
        if self.current_room.back_way:
            back_door = Door(280, 180, 80, 20, 'back')
            doors.append(back_door)
        return doors

    def move_point(self, dx=0, dy=0):
        old_x, old_y = self.point.x, self.point.y
        self.point.x += dx
        self.point.y += dy
        if self.check_wall_collision():
            self.point.x, self.point.y = old_x, old_y

    def check_wall_collision(self):
        point_rect = pygame.Rect(self.point.x - self.point.radius, self.point.y - self.point.radius,
                                 self.point.radius * 2, self.point.radius * 2)
        return any(wall.rect.colliderect(point_rect) for wall in self.walls)

    def actions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_point(dx=-self.point.speed)
        if keys[pygame.K_RIGHT]:
            self.move_point(dx=self.point.speed)
        if keys[pygame.K_UP]:
            self.move_point(dy=-self.point.speed)
        if keys[pygame.K_DOWN]:
            self.move_point(dy=self.point.speed)

    def check_if_on_doors(self):
        for door in self.doors:
            if door.rect.collidepoint(self.point.x, self.point.y):
                print(f"Collided with door: {door.direction}")
                self.change_room(door)
                break

    def change_room(self, door):
        new_room = None
        if door.direction == 'left':
            new_room = self.current_room.left_way
        elif door.direction == 'right':
            new_room = self.current_room.right_way
        elif door.direction == 'back':
            new_room = self.current_room.back_way

        if new_room is not None:
            self.current_room = new_room
            self.doors = self.update_doors()
            self.point.x = 320
            self.point.y = 240

    def character_rendering(self):
        # Draw a white circle on the screen at the point's position with its radius
        pygame.draw.circle(self.screen, (255, 255, 255), (self.point.x, self.point.y), self.point.radius)

    def room_rendering(self, room):
        for wall in self.walls:
            pygame.draw.rect(self.screen, (255, 255, 255), wall.rect)
        for door in self.doors:
            pygame.draw.rect(self.screen, (0, 255, 255), door.rect)

    def rendering(self):  # define a method to render (draw) the game state on the screen
        self.screen.fill((0, 0, 0))  # fill the screen with black color

        self.character_rendering()
        self.room_rendering(self.current_room)

        pygame.display.flip()  # update the screen
        pygame.time.Clock().tick(120)  # Limit the game to n frames per second

    def run(self):  # define the main game loop method
        running = True  # set the game to run
        while running:  # keep running the game loop until 'running' is False
            for event in pygame.event.get():  # process all events in the event queue
                if event.type == pygame.QUIT:  # if the window closure is triggered
                    running = False  # stop the game loop
            self.actions()  # call the 'actions' method to process keyboard inputs
            self.check_if_on_doors()
            self.rendering()  # call the 'rendering' method to draw the game state on the screen
        pygame.quit()  # end all pygame modules


game = Game()  # create an instance of the 'Game' class
game.run()  # start the game loop by calling the 'run' method of the game instance
