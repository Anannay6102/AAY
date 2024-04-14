import pygame
import random
import sys
import heapq

pygame.init()


class Point:
    """Represents a movable character in the game with a defined position, radius, and speed"""
    def __init__(self, radius, speed):  # Initialize attributes.
        self.x = 320  # Starting x-coordinate of the character on the screen.
        self.y = 20  # Starting y-coordinate of the character on the screen.
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
        self.colour = (0, 255, 255)  # Default color (cyan).
        self.direction = direction  # Direction of door, which define the next door 1
        if direction == 'exit':
            self.colour = (0, 255, 0)  # If it is exit door color is red.


class Room:
    _id_counter = 0
    """This class represents a room within a maze. Each room is essentially a node in a tree structure, with
    potential connections in three directions: back, left, and right. These connections are to other instances of Room,
    allowing for the dynamic construction of a maze."""
    def __init__(self, back_way=None):  # Initialize attributes
        self.id = Room._id_counter
        Room._id_counter += 1
        self.back_way = back_way  # Room from which this room was entered, if any (parent node)
        self.right_way = None  # Room that will be to the right of this room (right node)
        self.left_way = None  # Room that will be to the left of this room (left node)
        self.visited = False  # Status which shows if room was visited
        self.is_exit = False
        self.room_objects = []  # All objects of room, will be described in make_objects method
        self.spawn = (320, 25)  # The spawn coordinates are used when we visit a room several times

    def make_room_objects(self):  # Method which make doors and walls for this room.
        if self.left_way and self.right_way:
            self.room_objects.extend([Wall(210, 0, 10, 160), Wall(420, 0, 10, 160), Wall(210, 320, 10, 160),
                                      Wall(420, 320, 10, 160), Wall(0, 150, 210, 10), Wall(430, 150, 210, 10),
                                      Wall(0, 150, 10, 330), Wall(630, 150, 10, 330), Wall(220, 320, 200, 10),
                                      Wall(220, 0, 200, 10), Wall(10, 470, 200, 10), Wall(430, 470, 200, 10),
                                      Door(70, 460, 80, 10, 'left'), Door(490, 460, 80, 10, 'right')])
        elif self.left_way:
            self.room_objects.extend([Wall(210, 0, 10, 160), Wall(420, 0, 10, 320), Wall(220, 0, 200, 10),
                                      Wall(220, 320, 210, 10), Wall(210, 320, 10, 160), Wall(0, 150, 210, 10),
                                      Wall(0, 150, 10, 330), Wall(10, 470, 200, 10), Door(70, 460, 80, 10, 'left')])
        elif self.right_way:
            self.room_objects.extend([Wall(210, 0, 10, 330), Wall(420, 0, 10, 160), Wall(220, 0, 200, 10),
                                      Wall(220, 320, 200, 10), Wall(420, 320, 10, 160), Wall(430, 150, 210, 10),
                                      Wall(630, 150, 10, 330), Wall(430, 470, 200, 10),
                                      Door(490, 460, 80, 10, 'right')])
        else:
            self.room_objects.extend([Wall(210, 0, 10, 330), Wall(420, 0, 10, 330), Wall(220, 0, 200, 10),
                                      Wall(220, 320, 200, 10)])
        if self.back_way:
            self.room_objects.append(Door(280, 10, 80, 10, 'back'))
        else:
            self.visited = True


class Maze:
    """Constructs a tree/graph structure maze of 'Room' instances in a recursive manner. The maze is
       generated randomly, has configurations each time the function is called."""
    def __init__(self, size):
        self.size = size
        self.rooms = []
        self.start_room = self.generate_random_maze(self.size)
        self.leaf_rooms = []
        self.find_leaf_rooms(self.start_room)
        if self.leaf_rooms:
            self.exit_room = random.choice(self.leaf_rooms)
            self.exit_room.room_objects.append(Door(280, 310, 80, 10, 'exit'))
            self.exit_room.is_exit = True
        self.steps_to_exit = self.dijkstra_shortest_path()

    def generate_random_maze(self, size, back_way=None):
        """The maze's structure is determined by randomly splitting the remaining 'size' between the left and right path
        at each step until the base case of 'size' equal to 0 is reached.
        from https://www.geeksforgeeks.org/random-binary-tree-generator-using-python/"""
        if size == 0:  # If there are no more rooms to create,
            return None  # return None
        left_size = random.randint(0, size - 1)  # Randomly determine the size of the left branch of the maze.
        right_size = size - 1 - left_size  # The remaining size is allocated to the right branch.
        room = Room(back_way)  # Create the room
        room.left_way = self.generate_random_maze(left_size, room)  # Create left branches of maze from this room.
        room.right_way = self.generate_random_maze(right_size, room)  # Create right branches of maze from this room.
        room.make_room_objects()  # Create objects for this room.
        self.rooms.append(room)
        return room  # Return the current 'room' as the root of this segment of the maze.

    def find_leaf_rooms(self, room):
        if room is not None:
            if not room.left_way and not room.right_way:
                self.leaf_rooms.append(room)
            self.find_leaf_rooms(room.left_way)
            self.find_leaf_rooms(room.right_way)

    def dijkstra_shortest_path(self):
        # Dictionary to store the minimum cost to reach each room from the start room
        min_cost = {room: float('inf') for room in self.rooms}
        min_cost[self.start_room] = 0

        # Priority queue to explore the room with the smallest distance first
        priority_queue = [(0, self.start_room.id, self.start_room)]

        while priority_queue:
            current_cost, _, current_room = heapq.heappop(priority_queue)

            # Explore the neighbor rooms if a cheaper path to them is found
            for direction in ['left_way', 'right_way', 'back_way']:
                neighbor = getattr(current_room, direction)
                if neighbor is not None and min_cost[current_room] + 1 < min_cost[neighbor]:
                    min_cost[neighbor] = min_cost[current_room] + 1
                    heapq.heappush(priority_queue, (min_cost[neighbor], neighbor.id, neighbor))

        # The cost to reach the exit room
        return min_cost[self.exit_room]


class Game:
    """Main game class that encapsulates the game state and logic. It manages the game loop, character movements,
        collision detection, and rendering of game elements to the screen."""

    def __init__(self):  # initialize all attributes (features) of game
        self.point = Point(5, 5)  # Initialize the character with specified radius and speed.
        self.screen = pygame.display.set_mode((640, 480))  # Set the size of the game window.
        self.steps_to_exit = 0
        self.maze = Maze(7)
        self.current_room = self.maze.start_room  # Start the character in the initial room of the maze.
        self.room_objects = self.current_room.room_objects  # All current objects that will be interacted with.
        self.mini_game = MiniGame(self.screen)
        self.running = True

    def move_point(self):  # Method which moves point
        old_x, old_y = self.point.x, self.point.y  # Safe coordinates in case of wall_collision
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.point.x -= self.point.speed
        if keys[pygame.K_RIGHT]:
            self.point.x += self.point.speed
        if keys[pygame.K_UP]:
            self.point.y -= self.point.speed
        if keys[pygame.K_DOWN]:
            self.point.y += self.point.speed
        if self.check_wall_collision():
            self.point.x, self.point.y = old_x, old_y

    def check_wall_collision(self):
        walls = list(filter(lambda obj: isinstance(obj, Wall), self.room_objects))
        point_rect = pygame.Rect(self.point.x - self.point.radius, self.point.y - self.point.radius,
                                 self.point.radius * 2, self.point.radius * 2)
        return any(wall.figure.colliderect(point_rect) for wall in walls)

    def change_room(self, door):
        if door.direction == 'exit':
            self.game_over_menu()
        else:
            direction_to_room = {'left': (self.current_room.left_way, (110, 455)),
                                 'right': (self.current_room.right_way, (520, 455)),
                                 'back': (self.current_room.back_way, (320, 25))}
            new_room, self.current_room.spawn = direction_to_room[door.direction]
            if not new_room.visited:
                self.mini_game.run()
                new_room.visited = True
            self.point.x, self.point.y = new_room.spawn
            self.room_objects = new_room.room_objects
            self.current_room = new_room
            self.steps_to_exit += 1

    def game_logic(self):
        self.move_point()
        doors = list(filter(lambda obj: isinstance(obj, Door), self.room_objects))
        for door in doors:
            if door.figure.collidepoint(self.point.x, self.point.y):
                self.change_room(door)
                break

    def game_over_menu(self):
        message = f'{self.steps_to_exit} vs {self.maze.steps_to_exit}'
        text = pygame.font.Font(None, 36).render(message, True, (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.restart_game()
                    return
            self.screen.fill((0, 0, 0))
            self.screen.blit(text, (50, 50))
            pygame.display.flip()

    def restart_game(self):
        self.maze = Maze(7)
        self.current_room = self.maze.start_room
        self.room_objects = self.current_room.room_objects
        self.steps_to_exit = 0
        self.point = Point(5, 5)

    def render(self):  # Define a method to render (draw) the game state on the screen
        self.screen.fill((0, 0, 0))  # Fill the screen with black color
        pygame.draw.circle(self.screen, self.point.colour, (self.point.x, self.point.y), self.point.radius)
        for obj in self.room_objects:
            pygame.draw.rect(self.screen, obj.colour, obj.figure)  # Draw all room objects
        pygame.display.flip()  # Update the screen

    def run(self):  # Define the MAIN GAME LOOP method.
        while self.running:  # Keep running the game loop until 'running' is False.
            for event in pygame.event.get():  # Process all events in the event queue.
                if event.type == pygame.QUIT:  # If the window closure is triggered.
                    self.running = False  # Stop the game loop.
            self.render()  # Call the 'render' method to draw the game state on the screen.
            self.game_logic()


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


game = Game()  # create an instance of the 'Game' class
game.run()  # start the game loop by calling the 'run' method of the game instance
