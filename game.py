import pygame
import random

pygame.init()


class Room:
    """This class represents a room within a maze. Each room is essentially a node in a tree/graph structure, with
    potential connections in three directions: back, left, and right. These connections are to other instances of Room,
    allowing for the dynamic construction of a maze."""
    def __init__(self, number, back_way=None):  # Initialize attributes
        self.back_way = back_way  # Room from which this room was entered, if any (parent node)
        self.right_way = None  # Room that will be to the right of this room (right node)
        self.left_way = None  # Room that will be to the left of this room (left node)
        self.number = number  # Unique identifier for this room
        self.visited = False  # Status which shows if room was visited
        self.objects = []

    def make_objects(self):  # Method which make doors and walls for this room.
        self.objects = [Wall(0, 160, 640, 10), Wall(0, 320, 640, 10), Wall(0, 160, 10, 170), Wall(630, 160, 10, 170)]
        if self.left_way:  # Add a door to the left if the current room has a left connection.
            self.objects.append(Door(10, 200, 20, 80, 'left'))
        if self.right_way:  # Add a door to the right if the current room has a right connection.
            self.objects.append(Door(610, 200, 20, 80, 'right'))
        if self.back_way:  # Add a door at the back if the current room has a back connection.
            self.objects.append(Door(280, 170, 80, 20, 'back'))


def random_maze(size, back_way=None):
    """Constructs a tree/graph structure maze of 'Room' instances in a recursive manner. The maze is
    generated randomly, with the possibility of different configurations each time the function is called. The maze's
    structure is determined by randomly splitting the remaining 'size' between the left and right paths at each step
    until the base case of 'size' equal to 0 is reached.
    from https://www.geeksforgeeks.org/random-binary-tree-generator-using-python/"""
    if size == 0:  # If there are no more rooms to create,
        return None  # return None
    left_size = random.randint(0, size - 1)  # Randomly determine the size of the left branch of the maze.
    right_size = size - 1 - left_size  # The remaining size is allocated to the right branch.
    room = Room(size, back_way)  # Create the current room with the given 'size' as its identifier.
    room.left_way = random_maze(left_size, room)  # Recursively create the left branches of the maze from this room.
    room.right_way = random_maze(right_size, room)  # Recursively create the right branches of the maze from this room.
    room.make_objects()  # Create objects for this room.
    return room  # Return the current 'room' as the root of this segment of the maze.


class Point:
    """Represents a movable character in the game with a defined position, radius, and speed"""
    def __init__(self, radius, speed):  # Initialize attributes.
        self.x = 320  # Starting x-coordinate of the character on the screen.
        self.y = 240  # Starting y-coordinate of the character on the screen.
        self.radius = radius  # Radius of the circle representing the character.
        self.speed = speed  # Speed at which the character moves.
        self.colour = (255, 255, 255)  # Colour of point


class Wall:
    """Represents an immovable wall in the game. Walls define the boundaries and obstacles in rooms."""
    def __init__(self, x, y, width, height):  # Initialize attributes.
        self.figure = pygame.Rect(x, y, width, height)  # The rectangular area the wall occupies.
        self.colour = (255, 255, 255)  # Colour of wall


class Door:
    """Represents a door in the game, allowing the character to move between rooms."""
    def __init__(self, x, y, width, height, direction):  # Initialize attributes.
        self.figure = pygame.Rect(x, y, width, height)  # The rectangular area the door occupies.
        self.colour = (0, 255, 255)  # The rectangular area the door occupies.
        self.direction = direction  # Direction of door, which define the next door 1


class Game:
    """Main game class that encapsulates the game state and logic. It manages the game loop, character movements,
        collision detection, and rendering of game elements to the screen."""
    def __init__(self):  # initialize all attributes (features) of game
        self.point = Point(10, 5)  # Initialize the character with specified radius and speed.
        self.screen = pygame.display.set_mode((640, 480))  # Set the size of the game window.
        self.maze = random_maze(7)  # Generate a maze structure with 7 rooms.
        self.current_room = self.maze  # Start the character in the initial room of the maze.
        self.mini_game = MiniGame(self.screen)
        self.objects = self.current_room.objects  # All current objects that will be interacted with.

    def move_point(self, dx=0, dy=0):  # Method which moves point
        old_x, old_y = self.point.x, self.point.y  # Safe coordinates in case of wall_collision
        self.point.x += dx
        self.point.y += dy
        if self.check_wall_collision():
            self.point.x, self.point.y = old_x, old_y

    def keyboard_actions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_point(dx=-self.point.speed)
        if keys[pygame.K_RIGHT]:
            self.move_point(dx=self.point.speed)
        if keys[pygame.K_UP]:
            self.move_point(dy=-self.point.speed)
        if keys[pygame.K_DOWN]:
            self.move_point(dy=self.point.speed)

    def check_wall_collision(self):
        walls = list(filter(lambda obj: isinstance(obj, Wall), self.objects))
        point_rect = pygame.Rect(self.point.x - self.point.radius, self.point.y - self.point.radius,
                                 self.point.radius * 2, self.point.radius * 2)
        return any(wall.figure.colliderect(point_rect) for wall in walls)

    def change_room(self, door):
        new_room = None
        if door.direction == 'left':
            new_room = self.current_room.left_way
        elif door.direction == 'right':
            new_room = self.current_room.right_way
        elif door.direction == 'back':
            new_room = self.current_room.back_way
        self.current_room = new_room
        self.objects = self.current_room.objects
        if not self.current_room.visited:
            self.mini_game.run()
            self.current_room.visited = True
        self.point.x = 320
        self.point.y = 240

    def check_doors_opening(self):
        doors = list(filter(lambda obj: isinstance(obj, Door), self.objects))
        for door in doors:
            if door.figure.collidepoint(self.point.x, self.point.y):
                self.change_room(door)
                break

    def point_rendering(self):
        # Draw a white circle on the screen at the point's position with its radius
        pygame.draw.circle(self.screen, self.point.colour, (self.point.x, self.point.y), self.point.radius)

    def objects_rendering(self):
        for object in self.objects:
            pygame.draw.rect(self.screen, object.colour, object.figure)

    #def menu_rendering(self):

    def rendering(self):  # Define a method to render (draw) the game state on the screen
        self.screen.fill((0, 0, 0))  # Fill the screen with black color
        self.point_rendering()  # Draw point
        self.objects_rendering()  # Draw all room objects
        pygame.display.flip()  # Update the screen
        pygame.time.Clock().tick(120)  # Limit the game to n frames per second

    def run(self):  # Define the MAIN GAME LOOP method.
        running = True  # Set the game to run.
        while running:  # Keep running the game loop until 'running' is False.
            for event in pygame.event.get():  # Process all events in the event queue.
                if event.type == pygame.QUIT:  # If the window closure is triggered.
                    running = False  # Stop the game loop.
            self.keyboard_actions()  # Call the 'keyboard_actions' method to process keyboard inputs.
            self.check_doors_opening()  # Check if we open the door (if we locate on the door).
            self.rendering()  # Call the 'rendering' method to draw the game state on the screen.
        pygame.quit()  # End pygame module.


class MiniGame:
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        mini_game_running = True
        text = pygame.font.Font(None, 36).render('Press SPACE to finish the mini game', True, (255, 255, 255))
        while mini_game_running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    mini_game_running = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.screen.fill((0, 0, 0))
            self.screen.blit(text, (50, 50))
            pygame.display.flip()
            pygame.time.Clock().tick(60)


game = Game()  # create an instance of the 'Game' class
game.run()  # start the game loop by calling the 'run' method of the game instance
