import pygame
import random
import pdb

pygame.init()


class Stack:
    """
    A stack class that implements the basic operations of a stack data structure following the Last-in-First-Out
    (LIFO) principle. It is used to implement depth-first search (DFS) algorithms, as shown in the
    'find_length_of_shortest_path' and 'dfs_traversal' methods of the Maze class.
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
        return len(self.items)  # Returns the total number of elements in the stack


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
        self.visited = False  # Tracks whether the room has been visited by player, used in dfs algorithms.
        self.objects = []  # Holds the room's objects (walls, doors).
        self.spawn = (320, 30)  # Default spawn location for the point when entering the room.


class Maze:
    """
    Represents the overall maze structure in the game. It manages the creation, connectivity, and functionality
    of rooms, acting as a container for the entire maze through which the player navigates.
    """
    def __init__(self, size):
        self.size = size  # The size of the maze (number of rooms/nodes).
        self.rooms = []  # A list to store all room objects created during maze generation.
        self.leaf_rooms = []  # List to hold rooms that do not have child rooms, potential candidates for exits.
        self.start_room = self.generate_random_maze(self.size)  # Generates the maze starting from the root.
        self.find_leaf_rooms(self.start_room)  # Identifies all leaf rooms in the maze.
        self.exit_room = random.choice(self.leaf_rooms)  # Selects one of the leaf rooms to be the exit.
        self.make_objects()  # Places objects (walls and doors) in each room based on its connections.

    def generate_random_maze(self, size, back=None):
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

    def find_leaf_rooms(self, room):
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

    def find_length_of_shortest_path(self):
        """
        Calculate the length of the shortest path from a starting point to the exit room. The method assumes that there
        is a 'back' link in each room leading towards the starting room.
        """
        room = self.exit_room  # Initialize 'room' with the exit room.
        length = 0  # Initialize the length of the path as 0.
        while room:  # Loop until there are no more rooms linked with 'back'.
            length += 1  # Increment the path length by 1 for each room traversed.
            room = room.adjacent_rooms.get('back')  # Move to the adjacent room that is linked with 'back'.
        return length  # Return the total length of the path from the start to the exit.

    def find_visited_rooms_number(self):
        """
        A stack-based depth-first traversal of the maze, counting the number of rooms marked as visited by the player
        during gameplay, using LIFO data structure.
        """
        stack = Stack()   # Initialize a stack to manage the rooms during the depth-first traversal.
        stack.push(self.start_room)  # Start the traversal from the starting room.
        visited_rooms_count = 0  # Initialize a counter to keep track of rooms marked as visited.
        while not stack.is_empty():  # Continue until all rooms are visited.
            current_room = stack.pop()  # Pop the top room from the stack to explore it.
            if current_room.visited:  # If the room has been visited,
                visited_rooms_count += 1  # increment the count.
            # Check and add adjacent rooms to the stack for further exploration.
            for direction in ['left', 'right']:  # Only left and right directions are considered.
                adjacent_room = current_room.adjacent_rooms.get(direction)
                if adjacent_room:  # If there is an adjacent room,
                    stack.push(adjacent_room)  # push it to the stack for traversal.
        return visited_rooms_count  # Return the count of visited rooms.

    def get_next_room(self, current_room):
        """
        Determines the next room the player should move to from the current room to progress towards the exit. This
        method uses the concept of The Lowest Common Ancestor (LCA) algorithm to find the most direct path to the exit.
        """
        # Trace the path from the current room back to the root.
        room = current_room  # Safe
        path_to_current = []
        while room:
            path_to_current.append(room)
            room = room.adjacent_rooms.get('back')
        # Trace the path from the exit room back to the root.
        room = self.exit_room
        path_to_exit = []
        while room:
            path_to_exit.append(room)
            room = room.adjacent_rooms.get('back')

        '''# Debug:
        print("Path to current:", [id(r) for r in path_to_current])
        print("Path to exit:", [id(r) for r in path_to_exit])'''

        # Find the Lowest Common Ancestor (LCA) of the current room and the exit room.
        # The LCA is the last common room shared between the two paths traced above.
        lca = None
        while path_to_current and path_to_exit and path_to_current[-1] == path_to_exit[-1]:
            lca = path_to_current.pop()
            path_to_exit.pop()

        '''# Debug:
        print("LCA:", id(lca) if lca else "None")
        print("Popped path to current:", [id(r) for r in path_to_current])
        print("Popped path to exit:", [id(r) for r in path_to_exit])'''

        # Determine the next room to move towards based on the paths to the LCA. If there are rooms left in the
        # path_to_exit after finding the LCA, it means we need to move towards the exit from LCA. If there is more than
        # one room in the current path, the next room is the first room towards the LCA. Otherwise, select the next room
        # in the path to the exit, ensuring the movement is directed towards the exit.
        if len(path_to_exit) > 0:
            next_room = path_to_current[1] if len(path_to_current) > 1 else \
                (lca if len(path_to_current) > 0 else path_to_exit[-1])
            return next_room
        return current_room

    def make_objects(self):
        """
        After creating the structure of the maze, we add the necessary objects to each room based on their
        connections. The doors are in certain positions, this will help when getting a hint (get_hint Gamme class method
        """
        self.exit_room.objects.append(Door(280, 460, 80, 10, 'exit'))
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


class Game:
    """Main game class that encapsulates the game state and logic. It manages the game loop, character movements,
        collision detection, and rendering of game elements to the screen."""

    def __init__(self):  # initialize all attributes (features) of game
        self.point = Point()  # Initialize the character with specified radius and speed.
        self.screen = pygame.display.set_mode((640, 480))  # Set the size of the game window.
        self.maze = Maze(7)  # Create the maze with 7 rooms
        self.current_room = self.maze.start_room  # Start the character in the initial room of the maze.
        self.running = True

    def move_point(self):  # Method which moves point
        """
        Handles the movement of the player's character based on keyboard input. The function adjusts the character's
        position and checks for collisions with walls to prevent moving through them.
        """
        old_x, old_y = self.point.x, self.point.y  # Store old coordinates in case of collision.
        keys = pygame.key.get_pressed()  # Get the state of all keyboard keys.
        # Update character's position based on arrow keys pressed.
        if keys[pygame.K_LEFT]:
            self.point.x -= self.point.speed
        if keys[pygame.K_RIGHT]:
            self.point.x += self.point.speed
        if self.check_wall_collision():   # Revert to old position if collision occurs.
            # print('collision with a wall')
            self.point.x = old_x
        if keys[pygame.K_UP]:
            self.point.y -= self.point.speed
        if keys[pygame.K_DOWN]:
            self.point.y += self.point.speed
        if self.check_wall_collision():   # Revert to old position if collision occurs.
            # print('collision with a wall')
            self.point.y = old_y

    def check_wall_collision(self):
        """
        Checks for a collision between the player's character and any walls in the current room.
        Returns True if a collision is detected, preventing movement through walls.
        """
        # Check collision of the point's rectangle with each wall's rectangle.
        walls = list(filter(lambda obj: isinstance(obj, Wall), self.current_room.objects))
        # Create a rectangle for the point based on its position and radius.
        point_rect = pygame.Rect(self.point.x - self.point.radius, self.point.y - self.point.radius,
                                 self.point.radius * 2, self.point.radius * 2)
        return any(wall.figure.colliderect(point_rect) for wall in walls)

    def change_room(self, door):
        """
        Changes the current room of the game based on the door through which the character moves.
        This function updates the game state to reflect the new room and handles the spawn position
        of the character.
        """
        if door.direction == 'exit':
            self.game_over_menu()  # Trigger game over sequence if exiting the maze.
            return
        #  Save the position on the x-axis and also save the y coordinate by adding/taking 15, for the upper door (back)
        #  + for the lower ones - (left, right) to avoid continuous exit/entry into the room.
        spawn_offset = -15 if door.direction in ['left', 'right'] else 15
        # Set new spawn location in the current room
        self.current_room.spawn = (self.point.x, self.point.y + spawn_offset)
        new_room = self.current_room.adjacent_rooms[door.direction]  # Get the new room to enter.
        self.point.spawn = self.current_room.spawn  # Update the point's spawn position.
        self.point.x, self.point.y = new_room.spawn  # Move the point to the new room's spawn position.
        self.current_room = new_room  # Update the current room to the new room.
        if not new_room.visited:  # If the room has not been visited
            mini_game = MiniGame(self.screen)
            mini_game.run()  # run a mini-game if the room has not been visited.
            new_room.visited = True  # Mark the room as visited.

    def game_logic(self):
        """
        Contains the main logic of the game, which is called within the game loop. It manages the movement of the
        character, checks for interactions with doors, and changes room.
        """
        self.move_point()  # Handle character movement.
        doors = list(filter(lambda obj: isinstance(obj, Door), self.current_room.objects))  # List of all doors
        for door in doors:   # Check if the character interacts with any door.
            if door.figure.collidepoint(self.point.x, self.point.y):
                self.change_room(door)  # Change room if interacting with a door.
                break

    def get_hint(self):
        """
        Provides a hint to the player by highlighting the door that leads closer to the exit. This method determines
        which door in the current room points towards the exit by comparing the room positions in the maze's path.
        """
        #  pdb.set_trace()
        hint_room = self.maze.get_next_room(self.current_room)  # Determine the next room that leads towards the exit.
        left_room = self.current_room.adjacent_rooms.get('left')
        right_room = self.current_room.adjacent_rooms.get('right')
        back_room = self.current_room.adjacent_rooms.get('back')
        # Highlight the door leading to the next room based on the determined path by changing door color to green.
        if (left_room or right_room) and not (left_room and right_room):
            forward_room = left_room if left_room else right_room
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

    def game_over_menu(self):
        min_dis_path = self.maze.find_length_of_shortest_path()
        player_dis_path = self.maze.find_visited_rooms_number()
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
        self.point.x, self.point.y = (320, 30)

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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    self.get_hint()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.pause_menu()
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
