import pygame
import random
from collections import deque
import pdb
import pickle

from typing import List, Any, Tuple, Dict, Optional, Deque, Union, BinaryIO
from pygame import Rect, Surface, SurfaceType
from pygame.event import Event
from pygame.key import ScancodeWrapper

pygame.init()


class Stack:
    """
    A stack class that implements the basic operations of a stack data structure following the Last-in-First-Out
    (LIFO) principle. It is used to implement depth-first search (DFS) algorithms, as shown in the
    'find_visited_rooms_number' methods of the Maze class.
    """
    items: Deque[Any]

    def __init__(self):
        """
        Constructor for the Stack class. Initializes a new empty stack.
        """
        self.items = deque()  # This empty list will hold elements.

    def is_empty(self) -> bool:
        """
        Checks whether the stack is empty.
        """
        return len(self.items) == 0  # Returns True if there are no elements in the stack.

    def push(self, item: object):
        """
        Adds a new item to the top of the stack.
        """
        self.items.append(item)  # Adds the item to the end of the list, which represents the top of the stack.

    def pop(self) -> Optional[object]:
        """
        Removes and returns the top item of the stack if the stack is not empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self.items.pop()

    def peek(self) -> Optional[object]:
        """
        Returns the top item of the stack without removing it, if the stack is not empty.
        """
        if self.is_empty():  # Check if there are items before peeking to avoid accessing an empty list.
            raise IndexError("Peek from an empty stack")
        return self.items[-1]  # Returns the last element of the list without removing it.

    def size(self):
        """
        Returns the number of items in the stack.
        """
        return len(self.items)  # Returns the total number of elements in the stack


class Point:
    """
    Represents the player's character in the game, modeled as a movable point. This class is used for the game's
    dynamics, including movement and interaction with objects within the rooms.
    """
    x: int
    y: int
    radius: int
    speed: int
    colour: Tuple[int, int, int]

    def __init__(self):
        self.x = 320  # Starting x-coordinate of the character on the screen.
        self.y = 30  # Starting y-coordinate of the character on the screen.
        self.radius = 5  # Radius of the circle representing the character.
        self.speed = 5  # Speed at which the character moves.
        self.colour = (255, 255, 255)  # Colour of point (white).s


class Wall:
    """
    Represents an immovable wall in the game. Walls define the boundaries and obstacles in rooms. Prevents a point from
    passing through it, described in the check_wall_collision method of the game class.
    """
    figure: Rect
    colour: Tuple[int, int, int]

    def __init__(self, x: int, y: int, width: int, height: int):  # Initialize attributes.
        self.figure = pygame.Rect(x, y, width, height)  # The rectangular area the wall occupies.
        self.colour = (255, 255, 255)  # Colour of wall (white).


class Door:
    """
    Represents the passageways between rooms in the game, enabling the character to move across different parts of
    the maze.
    """
    figure: Rect
    colour: Tuple[int, int, int]
    direction: str

    def __init__(self, x: int, y: int, width: int, height: int, direction: str):
        self.figure = pygame.Rect(x, y, width, height)  # The rectangular area the door occupies.
        self.colour = (0, 255, 255)  # Default color (cyan).
        self.direction = direction  # Direction of door, which define the next room


class Room:
    """
    Represents a room within the maze, which is essentially a node in the game's tree structure. Rooms contain objects
    like walls and doors, and link to other rooms, shaping the maze's pathways.
    """
    adjacent_rooms: Dict[str, Optional[any]]
    visited: bool
    objects: List[Wall or Door]
    spawn: Tuple[int, int]

    def __init__(self, back: any):
        self.adjacent_rooms = {'back': back, 'right': None, 'left': None}  # Connections to adjacent rooms.
        self.visited = False  # Tracks whether the room has been visited by player, used in dfs algorithms.
        self.objects = []  # Holds the room's objects (walls, doors).
        self.spawn = (320, 30)  # Default spawn location for the point when entering the room.


class Maze:
    """
    Represents the overall maze structure in the game, which is a tree data structure. It manages the creation,
    connectivity, and functionality of rooms, acting as a container for the entire maze info through which the player
    navigates.
    """
    size: int
    rooms: List[Room]
    leaf_rooms: List[Room]
    start_room: Room
    exit_room: Room

    def __init__(self, size: int):
        self.size = size  # The size of the maze (number of rooms/nodes).
        self.rooms = []  # A list to store all room objects created during maze generation.
        self.leaf_rooms = []  # List to hold rooms that do not have child rooms, potential candidates for exits.
        self.start_room = self.generate_random_maze(self.size)  # Generates the maze starting from the root.
        self.find_leaf_rooms(self.start_room)  # Identifies all leaf rooms in the maze.
        self.exit_room = random.choice(self.leaf_rooms)  # Selects one of the leaf rooms to be the exit.
        self.make_objects()  # Places objects (walls and doors) in each room based on its connections.
        self.print_maze_debug_info(debug=False)

    def generate_random_maze(self, size: int, back: Room = None) -> Room or None:
        """
        Recursively generates a random maze structure. It uses a binary tree generation logic where each room can split
        into two child rooms (left and right).
        """
        if size == 0:  # Do nothing if subtree do not have rooms/nodes
            return None
        left_size = random.randint(0, size - 1)  # Randomly determine the number of rooms in the left subtree.
        right_size = size - 1 - left_size  # The remaining rooms go into the right subtree.
        room = Room(back)  # Create a new room, setting its back connection to its parent.
        room.adjacent_rooms['left'] = self.generate_random_maze(left_size, room)  # Recursively generate left child.
        room.adjacent_rooms['right'] = self.generate_random_maze(right_size, room)  # Recursively generate right child.
        self.rooms.append(room)  # Add the newly created room to the maze's room list.
        return room  # Return the processed root with children

    def find_leaf_rooms(self, room) -> None:
        """
        Recursively identifies rooms that do not have any children (leaf rooms), which are potential exit points.
        """
        if room is not None:  # If room exists then
            if not room.adjacent_rooms['right'] and not room.adjacent_rooms['left']:  # If node do not have children
                self.leaf_rooms.append(room)  # it means that this is leaf node, so add to leaf rooms list
            if room.adjacent_rooms['left']:  # If node has left child then
                self.find_leaf_rooms(room.adjacent_rooms['left'])  # Check that left child for leaf rooms
            if room.adjacent_rooms['right']:  # If node has right child then
                self.find_leaf_rooms(room.adjacent_rooms['right'])  # Check that right child for leaf rooms

    def find_length_of_shortest_path(self) -> int:
        """
        Calculate the length of the shortest path from a starting point to the exit room. The method assumes that there
        is a 'back' link in each room leading towards the starting room.
        """
        room = self.exit_room  # Initialize 'room' with the exit room.
        length: int = 0  # Initialize the length of the path as 0.
        while room:  # Loop until there are no more rooms linked with 'back'.
            length += 1  # Increment the path length by 1 for each room traversed.
            room = room.adjacent_rooms.get('back')  # Move to the adjacent room that is linked with 'back'.
        return length  # Return the total length of the path from the start to the exit.

    def find_visited_rooms_number(self, **kwargs) -> int:
        """
        A stack-based depth-first traversal of the maze, counting the number of rooms marked as visited by the player
        during gameplay, using LIFO data structure.
        """
        stack: Stack = Stack()  # Initialize a stack to manage the rooms during the depth-first traversal.
        stack.push(self.start_room)  # Start the traversal from the starting room.
        visited_rooms_count: int = 0  # Initialize a counter to keep track of rooms marked as visited.
        while not stack.is_empty():  # Continue until all rooms are visited.
            current_room = stack.pop()  # Pop the top room from the stack to explore it.
            if current_room.visited:  # If the room has been visited,
                visited_rooms_count += 1  # increment the count.
            # Check and add adjacent rooms to the stack for further exploration.
            for direction in ['left', 'right']:  # Only left and right directions are considered.
                adjacent_room = current_room.adjacent_rooms.get(direction)
                if adjacent_room:  # If there is an adjacent room,
                    stack.push(adjacent_room)  # push it to the stack for traversal.

                if kwargs.get('debug'):
                    # Print the current stack's content by showing each room's status
                    stack_contents = [room.visited for room in stack.items]
                    print(f"Current stack (from top to bottom): {stack_contents}")
        if kwargs.get('debug'):
            print(f"Visited rooms count: {visited_rooms_count}")
            for room in self.rooms:
                if room.visited:
                    print(id(room))

        return visited_rooms_count  # Return the count of visited rooms.

    def get_next_room(self, current_room: Room, **kwargs) -> Room:
        """
        Determines the next room the player should move to from the current room to progress towards the exit. This
        method uses the concept of The Lowest Common Ancestor (LCA) algorithm to find the most direct path to the exit.
        This method is used to give the player a hint, as described in the get_hint game class.
        """
        room: Room = current_room
        path_to_current: List[Room] = []  # Trace the path from the current room back to the root.
        while room:  # Loop until there are no more rooms linked with 'back'.
            path_to_current.append(room)  # Add this room to path list
            room = room.adjacent_rooms.get('back')  # Move to the adjacent room that is linked with 'back'.
        room = self.exit_room
        path_to_exit: List[Room] = []  # Trace the path from the exit room back to the root.
        while room:  # Loop until there are no more rooms linked with 'back'.
            path_to_exit.append(room)  # Add this room to path list
            room = room.adjacent_rooms.get('back')  # Move to the adjacent room that is linked with 'back'.

        if kwargs.get('debug'):
            print("Path to current:", [id(r) for r in path_to_current])
            print("Path to exit:", [id(r) for r in path_to_exit])

        # Find the Lowest Common Ancestor (LCA) of the current room and the exit room.
        # The LCA is the last common room shared between the two paths traced above.
        lca: Room or None = None
        while path_to_current and path_to_exit and path_to_current[-1] == path_to_exit[-1]:
            lca = path_to_current.pop()
            path_to_exit.pop()

        if kwargs.get('debug'):
            print("LCA:", id(lca) if lca else "None")
            print("Popped path to current:", [id(r) for r in path_to_current])
            print("Popped path to exit:", [id(r) for r in path_to_exit])

        # Determine the next room to move towards based on the paths to the LCA. If there are rooms left in the
        # path_to_exit after finding the LCA, it means that there are some rooms between the exit and the current room,
        # otherwise we are already in exit room. If there is more than one room in the current path, the next room is
        # the first room towards the LCA. Otherwise, the current room is LCA, therefore, we return the next room leading
        # to the exit
        if len(path_to_exit) > 0:
            next_room: Optional[Room] = path_to_current[1] if len(path_to_current) > 1 else \
                (lca if len(path_to_current) > 0 else path_to_exit[-1])
        else:
            next_room = current_room
        if kwargs.get('debug'):
            print("Next room to move to:", id(next_room))

        return next_room

    def make_objects(self) -> None:
        """
        After creating the structure of the maze, we add the necessary objects to each room based on their
        connections. The doors are in certain positions, this will help when getting a hint (get_hint Game class method)
        """
        self.exit_room.objects.append(Door(280, 460, 80, 10, 'exit'))
        room: Room
        for room in self.rooms:
            if room.adjacent_rooms['back']:
                room.objects.append(Door(280, 10, 80, 10, 'back'))
            else:
                room.visited = True
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

    def print_maze_debug_info(self, **kwargs):
        if kwargs.get('debug', False):  # Only execute if debug is explicitly set to True
            print('Maze Configuration:')
            for room in self.rooms:  # Check if detailed output is requested
                neighbors = {key: (id(adj_room) if adj_room else "No Room")
                             for key, adj_room in room.adjacent_rooms.items()}
                print(f'Room at {id(room)} has neighbors: {neighbors}')
            print(f'Start room: {id(self.start_room)}')
            print(f'Exit room: {id(self.exit_room)}')


class Game:
    """Main game class that encapsulates the game state and logic. It manages the game loop, character movements,
        collision detection, and rendering of game elements to the screen."""
    point: Point
    screen: Union[Surface, SurfaceType]
    maze: Maze
    current_room: Room
    running: bool

    def __init__(self):
        self.point = Point()  # Initialize the character.
        self.screen = pygame.display.set_mode((640, 480))  # Set the size of the game window.
        self.maze = Maze(7)  # Create the maze with 7 rooms
        self.current_room = self.maze.start_room  # Start the character in the initial room of the maze.
        self.running = True  # Flag for execution of game

    def move_point(self, **kwargs) -> None:  # Method which moves point
        """
        Handles the movement of the player's character based on keyboard input. The function adjusts the character's
        position and checks for collisions with walls to prevent moving through them.
        """
        old_x: int
        old_y: int
        old_x, old_y = self.point.x, self.point.y  # Store old coordinates in case of collision.
        keys: ScancodeWrapper = pygame.key.get_pressed()  # Get the state of all keyboard keys.
        # Update character's position based on arrow keys pressed.
        if keys[pygame.K_LEFT]:
            self.point.x -= self.point.speed
        if keys[pygame.K_RIGHT]:
            self.point.x += self.point.speed
        if self.check_wall_collision(**kwargs):  # Revert to old position if collision occurs.
            self.point.x = old_x
        if keys[pygame.K_UP]:
            self.point.y -= self.point.speed
        if keys[pygame.K_DOWN]:
            self.point.y += self.point.speed
        if self.check_wall_collision(**kwargs):  # Revert to old position if collision occurs.
            self.point.y = old_y
        if kwargs.get('debug'):
            print(f"Moved to {self.point.x}, {self.point.y}")
        # I have specifically separated the detection of collisions with walls by coordinates so that the point can
        # slide along the walls

    def check_wall_collision(self, **kwargs) -> bool:
        """
        Checks for a collision between the player's character and any walls in the current room.
        Returns True if a collision is detected, preventing movement through walls.
        """
        # Check collision of the point's rectangle with each wall's rectangle.
        walls: List[Wall] = list(filter(lambda obj: isinstance(obj, Wall), self.current_room.objects))
        # Create a rectangle for the point based on its position and radius.
        point_rect: Rect = pygame.Rect(self.point.x - self.point.radius, self.point.y - self.point.radius,
                                       self.point.radius * 2, self.point.radius * 2)
        collision = any(wall.figure.colliderect(point_rect) for wall in walls)
        if collision and kwargs.get('debug'):
            print(f"Collision detected at ({self.point.x}, {self.point.y}) with a wall.")
        return collision

    def change_room(self, door: Door) -> None:
        """
        Changes the current room of the game based on the door through which the character moves.
        This function updates the game state to reflect the new room and handles the spawn position
        of the character.
        """
        if door.direction == 'exit':
            self.game_over_menu()  # Trigger game over sequence if exiting the maze.
            return
        #  Save the position on the x-axis and also save the y coordinate by adding/taking 15, adding for the upper door
        #  (back) and taking for the lower ones (left, right) to avoid continuous exit/entry into the room.
        spawn_offset: int = -15 if door.direction in ['left', 'right'] else 15
        # Set new spawn location in the current room
        self.current_room.spawn = (self.point.x, self.point.y + spawn_offset)
        new_room: Room = self.current_room.adjacent_rooms[door.direction]  # Get the new room to enter.
        self.point.x, self.point.y = new_room.spawn  # Move the point to the new room's spawn position.
        self.current_room = new_room  # Update the current room to the new room.
        if not new_room.visited:  # If the room has not been visited
            mini_game: MiniGame = MiniGame(self.screen)
            mini_game.run()  # run a mini-game if the room has not been visited.
            new_room.visited = True  # Mark the room as visited.

    def game_logic(self) -> None:
        """
        Contains the main logic of the game, which is called within the game loop. It manages the movement of the
        character, checks for interactions with doors, and changes room.
        """
        self.move_point(debug=False)  # Handle character movement.
        # List of all doors
        doors: List[Door] = list(filter(lambda obj: isinstance(obj, Door), self.current_room.objects))
        door: Door
        for door in doors:  # Check if the character interacts with any door.
            if door.figure.collidepoint(self.point.x, self.point.y):
                self.change_room(door)  # Change room if interacting with a door.
                break
        self.render()  # Draw the game state to the screen

    def get_hint(self):
        """
        Provides a hint to the player by highlighting the door that leads closer to the exit. This method determines
        which door in the current room points towards the exit by comparing the room positions in the maze's path.
        """
        # pdb.set_trace()
        # Determine the next room that leads towards the exit.
        hint_room: Room = self.maze.get_next_room(self.current_room, debug=False)
        left_room: Room = self.current_room.adjacent_rooms.get('left')
        right_room: Room = self.current_room.adjacent_rooms.get('right')
        back_room: Room = self.current_room.adjacent_rooms.get('back')
        # Highlight the door leading to the next room based on the determined path by changing door color to green.
        if (left_room or right_room) and not (left_room and right_room):
            forward_room: Room = left_room if left_room else right_room
            if hint_room == forward_room:
                self.current_room.objects[-1].colour = (0, 255, 0)
            elif hint_room == back_room:
                self.current_room.objects[0].colour = (0, 255, 0)
            else:
                self.current_room.objects[0].colour = (0, 255, 0)
        else:
            if hint_room == left_room:
                self.current_room.objects[-2].colour = (0, 255, 0)
            elif hint_room == right_room:
                self.current_room.objects[-1].colour = (0, 255, 0)
            elif hint_room == back_room:
                self.current_room.objects[0].colour = (0, 255, 0)
            else:
                self.current_room.objects[0].colour = (0, 255, 0)

    def restart_game(self) -> None:
        """
        Restarts the game by reinitializing the maze and resetting the player's position to the starting point.
        """
        self.maze = Maze(7)  # Reinitialize the maze.
        self.current_room = self.maze.start_room  # Reset the current room to the start.
        self.point.x, self.point.y = (320, 30)  # Reset the player's position.

    def render(self) -> None:
        """
        Renders the current state of the game to the screen, including the player's character and any objects
        within the current room.
        """
        self.screen.fill((0, 0, 0))  # Clear the screen with black.
        # Draw the player's character as a circle on the screen.
        pygame.draw.circle(self.screen, self.point.colour, (self.point.x, self.point.y), self.point.radius)
        # Draw each object in the current room.
        for obj in self.current_room.objects:
            pygame.draw.rect(self.screen, obj.colour, obj.figure)

        # Draw indicating text
        text1: Union[Surface, SurfaceType] = pygame.font.Font(None, 20).render(f'Press h to get the hint', True,
                                                                               (255, 255, 255))
        text2: Union[Surface, SurfaceType] = pygame.font.Font(None, 20).render(f'Press p to open the menu', True,
                                                                               (255, 255, 255))
        self.screen.blit(text1, (10, 10))
        self.screen.blit(text2, (10, 25))
        pygame.display.flip()  # Update the display to show the new drawings.

    def save_game(self) -> None:
        """
        Saves the current game state to a file named 'save-game.dat' using the pickle module.
        The attributes saved include: the maze configuration, the current room, and the coordinates (x, y) of the point.
        """
        # Open the file in binary write mode
        with open('save-game.dat', 'wb') as f:
            pickle.dump({
                'maze': self.maze,                  # the game's maze structure
                'current_room': self.current_room,  # the current room in the maze
                'point_x': self.point.x,            # x-coordinate of the point
                'point_y': self.point.y             # y-coordinate of the point
            }, f)
        print("Game saved successfully!")

    def load_game(self) -> None:
        """
        Loads the game state from the file 'save-game.dat' using the pickle module. Restores attribute like maze
        configuration, current room, and coordinates (x, y) of the point.
        """
        # Open the file in binary read mode
        with open('save-game.dat', 'rb') as f:
            data: object = pickle.load(f)
            self.maze = data['maze']
            self.current_room = data['current_room']
            self.point.x = data['point_x']
            self.point.y = data['point_y']
        print("Game loaded successfully!")

    def options_menu(self):
        """
        Displays the options menu using Pygame and handles user input for various game operations,
        including quit, restart, save, load, and continue.
        """
        while True:
            # Render the various options on the screen
            text1: Union[Surface, SurfaceType] = pygame.font.Font(None, 36).render('Press Q to Quit', True,
                                                                                   (255, 255, 255))
            text2: Union[Surface, SurfaceType] = pygame.font.Font(None, 36).render('Press R to Restart', True,
                                                                                   (255, 255, 255))
            text3: Union[Surface, SurfaceType] = pygame.font.Font(None, 36).render('Press S to Save', True,
                                                                                   (255, 255, 255))
            text4: Union[Surface, SurfaceType] = pygame.font.Font(None, 36).render('Press L to Load', True,
                                                                                   (255, 255, 255))
            text5: Union[Surface, SurfaceType] = pygame.font.Font(None, 36).render('Press C to Continue', True,
                                                                                   (255, 255, 255))
            self.screen.fill((0, 0, 0))
            self.screen.blit(text1, (50, 50))
            self.screen.blit(text2, (50, 75))
            self.screen.blit(text3, (50, 100))
            self.screen.blit(text4, (50, 125))
            self.screen.blit(text5, (50, 150))
            pygame.display.flip()
            # Event handling for keyboard input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                        return
                    elif event.key == pygame.K_r:
                        self.restart_game()
                        return
                    elif event.key == pygame.K_s:
                        self.save_game()
                        return
                    elif event.key == pygame.K_l:
                        self.load_game()
                        return
                    elif event.key == pygame.K_c:
                        return
                elif event.type is pygame.QUIT:
                    self.running = False
                    return

    def game_over_menu(self) -> None:
        """
        Displays the game over menu when the player exits the maze. It calculates and displays the player's score based
        on the shortest path to the exit compared to the path the player took. It also provides options to quit or
        restart the game.
        """
        # Calculate the shortest possible path to the exit and number of visited rooms by player.
        min_dis_path: int = self.maze.find_length_of_shortest_path()
        player_dis_path: int = self.maze.find_visited_rooms_number(debug=False)
        score: int = int(min_dis_path / player_dis_path * 100)  # Compute the score as a percentage.
        # Render text with the player's score and instructions for quitting or restarting.
        text1: Union[Surface, SurfaceType] = pygame.font.Font(None, 36).render(f'Your score: {score}', True,
                                                                               (255, 255, 255))
        text2: Union[Surface, SurfaceType] = pygame.font.Font(None, 36).render(f'Press Q to quit the game', True,
                                                                               (255, 255, 255))
        text3: Union[Surface, SurfaceType] = pygame.font.Font(None, 36).render(f'Press R to restart the game', True,
                                                                               (255, 255, 255))
        while True:
            event: Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    self.running = False  # Stop the game loop if quiting game
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart_game()  # Restart the game by reinitializing the maze and game state, if triggerd.
                    return
            self.screen.fill((0, 0, 0))
            self.screen.blit(text1, (50, 50))
            self.screen.blit(text2, (50, 75))
            self.screen.blit(text3, (50, 100))
            pygame.display.flip()

    def run(self) -> None:
        """
        Main game loop that processes events, updates game logic, and renders the game state until the game is stopped.
        """
        while self.running:  # Continue running the game until the running flag is set to False.
            event: Event
            for event in pygame.event.get():  # Process all events in the pygame event queue.
                if event.type == pygame.QUIT:
                    self.running = False  # Stop the game loop if quiting game.
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    self.get_hint()  # Display a hint if 'h' is pressed.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.options_menu()  # Display a menu if 'p' is pressed.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.maze.print_maze_debug_info(debug=True)  # Display debug statements if 'd' pressed.
                    self.maze.find_visited_rooms_number(debug=True)
                    self.maze.get_next_room(self.current_room, debug=True)

            self.game_logic()  # Update the game logic.
        pygame.quit()


class MiniGame:
    def __init__(self, screen):
        self.screen = screen

    def run(self) -> None:
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
