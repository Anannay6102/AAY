import pygame
import random


pygame.init()


class Stack:
    """
    A stack class that implements the basic operations of a stack data structure following the Last-in-First-Out
    (LIFO) principle. It is used to implement depth-first search (DFS) algorithms, as shown in the 'dfs_search' and
    'dfs_traversal' methods of the Maze class.
    """

    def __init__(self):
        """
        Constructor for the Stack class. Initializes a new empty stack.
        """
        self.items = []  # This empty list will hold elements such as room and path length tuples.

    def is_empty(self):
        """
        Checks whether the stack is empty.
        """
        return len(self.items) == 0  # Returns True if there are no elements in the stack.

    def push(self, item):
        """
        Adds a new item to the top of the stack.
        """
        self.items.append(item)  # Adds the item to the end of the list, which represents the top of the stack.

    def pop(self):
        """
        Removes and returns the top item of the stack if the stack is not empty.
        """
        if not self.is_empty():  # Check if the stack has elements before popping to avoid errors.
            return self.items.pop()  # Removes the last item from the list and returns it.

    def peek(self):
        """
        Returns the top item of the stack without removing it, if the stack is not empty.
        """
        if not self.is_empty():  # Check if there are items before peeking to avoid accessing an empty list.
            return self.items[-1]  # Returns the last element of the list without removing it.

    def size(self):
        """
        Returns the number of items in the stack.
        """
        return len(self.items)  # Returns the total number of elements in the


class Point:
    """
    Represents the player's character in the game, modeled as a movable point. This class is used for the game's
    dynamics, including movement and interaction with objects within the rooms.
    """
    def __init__(self):
        self.x = 320  # Starting x-coordinate of the character on the screen.
        self.y = 30  # Starting y-coordinate of the character on the screen.
        self.radius = 5  # Radius of the circle representing the character.
        self.speed = 5  # Speed at which the character moves.
        self.colour = (255, 255, 255)  # Colour of point (white).


class Wall:
    """
    Represents an immovable wall in the game. Walls define the boundaries and obstacles in rooms. Prevents a point from
    passing through it, described in the check_wall_collision method of the game class.
    """
    def __init__(self, x, y, width, height):  # Initialize attributes.
        self.figure = pygame.Rect(x, y, width, height)  # The rectangular area the wall occupies.
        self.colour = (255, 255, 255)  # Colour of wall (white).


class Door:
    """
    Represents the passageways between rooms in the game, enabling the character to move across different parts of
    the maze.
    """
    def __init__(self, x, y, width, height, direction):  # Initialize attributes.
        self.figure = pygame.Rect(x, y, width, height)  # The rectangular area the door occupies.
        self.colour = (0, 255, 255)  # Default color (cyan).
        self.direction = direction  # Direction of door, which define the next room


class Room:
    """
    Represents a room within the maze, which is essentially a node in the game's graph structure. Rooms contain objects
    like walls and doors, and link to other rooms, shaping the maze's pathways.
    """
    def __init__(self, back=None):
        self.adjacent_rooms = {'back': back, 'right': None, 'left': None}  # Connections to adjacent rooms.
        self.visited = False  # Tracks whether the room has been visited by player, used in dfs_traversal algorithms.
        self.objects = []  # Holds the room's objects (walls, doors).
        self.spawn = (320, 30)  # Default spawn location for the point when entering the room.


class Maze:
    def __init__(self, size):
        self.size = size
        self.rooms = []
        self.leaf_rooms = []
        self.start_room = self.generate_random_maze(self.size)
        self.find_leaf_rooms(self.start_room)
        self.exit_room = self.find_exit_room()
        self.make_objects()

    def generate_random_maze(self, size, back=None):
        """from https://www.geeksforgeeks.org/random-binary-tree-generator-using-python/"""
        if size == 0:
            return None
        left_size = random.randint(0, size - 1)
        right_size = size - 1 - left_size
        room = Room(back)
        room.adjacent_rooms['left'] = self.generate_random_maze(left_size, room)
        room.adjacent_rooms['right'] = self.generate_random_maze(right_size, room)
        self.rooms.append(room)
        return room

    def find_leaf_rooms(self, room):
        if room is not None:
            if not room.adjacent_rooms['right'] and not room.adjacent_rooms['left']:
                self.leaf_rooms.append(room)
            if room.adjacent_rooms['left']:
                self.find_leaf_rooms(room.adjacent_rooms['left'])
            if room.adjacent_rooms['right']:
                self.find_leaf_rooms(room.adjacent_rooms['right'])

    def find_exit_room(self):
        exit_room = random.choice(self.leaf_rooms)
        exit_room.objects.append(Door(280, 460, 80, 10, 'exit'))
        return exit_room

    def dfs_search(self):
        stack = Stack()
        stack.push((self.start_room, 1))
        checked = set()
        while not stack.is_empty():
            current_room, current_path_length = stack.pop()
            if current_room in checked:
                continue
            checked.add(current_room)
            if current_room == self.exit_room:
                return current_path_length
            for adjacent_room in current_room.adjacent_rooms.values():
                if adjacent_room is not None and adjacent_room not in checked:
                    stack.push((adjacent_room, current_path_length + 1))

    def dfs_traversal(self):
        stack = Stack()
        stack.push(self.start_room)
        checked = set()  # Keep track of visited rooms to avoid processing them again
        visited_rooms_count = 0  # Counter for rooms with visited == True
        while not stack.is_empty():
            current_room = stack.pop()
            if current_room in checked:
                continue
            checked.add(current_room)
            if current_room and current_room.visited:
                visited_rooms_count += 1
                # Push adjacent rooms to the stack if they haven't been visited
            for adjacent_room in current_room.adjacent_rooms.values():
                if adjacent_room is not None and adjacent_room not in checked:
                    stack.push(adjacent_room)
        return visited_rooms_count

    def make_objects(self):
        for room in self.rooms:
            if room.adjacent_rooms['left'] and room.adjacent_rooms['right']:
                room.objects.extend([Wall(210, 0, 10, 160), Wall(420, 0, 10, 160), Wall(210, 320, 10, 160),
                                     Wall(420, 320, 10, 160), Wall(0, 150, 210, 10), Wall(430, 150, 210, 10),
                                     Wall(0, 150, 10, 330), Wall(630, 150, 10, 330), Wall(220, 320, 200, 10),
                                     Wall(220, 0, 200, 10), Wall(10, 470, 200, 10), Wall(430, 470, 200, 10),
                                     Door(70, 460, 80, 10, 'left'), Door(490, 460, 80, 10, 'right')])
            elif room.adjacent_rooms['left']:
                room.objects.extend([Wall(210, 0, 10, 640), Wall(420, 0, 10, 640), Wall(220, 0, 200, 10),
                                     Wall(220, 470, 200, 10), Door(280, 460, 80, 10, 'left')])
            elif room.adjacent_rooms['right']:
                room.objects.extend([Wall(210, 0, 10, 640), Wall(420, 0, 10, 640), Wall(220, 0, 200, 10),
                                     Wall(220, 470, 200, 10), Door(280, 460, 80, 10, 'right')])
            else:
                room.objects.extend([Wall(210, 0, 10, 640), Wall(420, 0, 10, 640), Wall(220, 0, 200, 10),
                                     Wall(220, 470, 200, 10)])
            if room.adjacent_rooms['back']:
                room.objects.append(Door(280, 10, 80, 10, 'back'))
            else:
                room.visited = True


class Game:
    """Main game class that encapsulates the game state and logic. It manages the game loop, character movements,
        collision detection, and rendering of game elements to the screen."""

    def __init__(self):  # initialize all attributes (features) of game
        self.point = Point()  # Initialize the character with specified radius and speed.
        self.screen = pygame.display.set_mode((640, 480))  # Set the size of the game window.
        self.maze = Maze(7)
        self.current_room = self.maze.start_room  # Start the character in the initial room of the maze.
        self.mini_game = MiniGame(self.screen)
        self.running = True

    def move_point(self):  # Method which moves point
        old_x, old_y = self.point.x, self.point.y  # Safe coordinates in case of wall_collision
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.point.x -= self.point.speed
        if keys[pygame.K_RIGHT]:
            self.point.x += self.point.speed
        if self.check_wall_collision():
            self.point.x = old_x
        if keys[pygame.K_UP]:
            self.point.y -= self.point.speed
        if keys[pygame.K_DOWN]:
            self.point.y += self.point.speed
        if self.check_wall_collision():
            self.point.y = old_y

    def check_wall_collision(self):
        walls = list(filter(lambda obj: isinstance(obj, Wall), self.current_room.objects))
        point_rect = pygame.Rect(self.point.x - self.point.radius, self.point.y - self.point.radius,
                                 self.point.radius * 2, self.point.radius * 2)
        return any(wall.figure.colliderect(point_rect) for wall in walls)

    def change_room(self, door):
        if door.direction == 'exit':
            self.game_over_menu()
            return
        spawn_offset = -15 if door.direction in ['left', 'right'] else 15
        self.current_room.spawn = (self.point.x, self.point.y + spawn_offset)
        new_room = self.current_room.adjacent_rooms[door.direction]
        self.point.spawn = self.current_room.spawn
        self.point.x, self.point.y = new_room.spawn
        self.current_room = new_room
        if not new_room.visited:
            self.mini_game.run()
            new_room.visited = True

    def game_logic(self):
        self.move_point()
        doors = list(filter(lambda obj: isinstance(obj, Door), self.current_room.objects))
        for door in doors:
            if door.figure.collidepoint(self.point.x, self.point.y):
                self.change_room(door)
                break
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.pause_menu()

    def game_over_menu(self):
        min_dis_path = self.maze.dfs_search()
        player_dis_path = self.maze.dfs_traversal()
        score = int(min_dis_path/player_dis_path*100)
        text1 = pygame.font.Font(None, 36).render(f'Your score: {score}', True, (255, 255, 255))
        text2 = pygame.font.Font(None, 36).render(f'Press q to quit the game', True, (255, 255, 255))
        text3 = pygame.font.Font(None, 36).render(f'Press r to restart the game', True, (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart_game()
                    return
            self.screen.fill((0, 0, 0))
            self.screen.blit(text1, (50, 50))
            self.screen.blit(text2, (50, 75))
            self.screen.blit(text3, (50, 100))
            pygame.display.flip()

    def pause_menu(self):
        text1 = pygame.font.Font(None, 36).render(f'Press q to quit the game', True, (255, 255, 255))
        text2 = pygame.font.Font(None, 36).render(f'Press r to restart the game', True, (255, 255, 255))
        text3 = pygame.font.Font(None, 36).render(f'Press c to proceed the game', True, (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart_game()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    return
            self.screen.fill((0, 0, 0))
            self.screen.blit(text1, (50, 50))
            self.screen.blit(text2, (50, 75))
            self.screen.blit(text3, (50, 100))
            pygame.display.flip()

    def restart_game(self):
        self.maze = Maze(7)
        self.current_room = self.maze.start_room
        self.point.x, self.point.y = 320, 30

    def render(self):  # Define a method to render (draw) the game state on the screen
        self.screen.fill((0, 0, 0))  # Fill the screen with black color
        pygame.draw.circle(self.screen, self.point.colour, (self.point.x, self.point.y), self.point.radius)
        for obj in self.current_room.objects:
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
