import pygame


class Point:  # make object point (character)
    def __init__(self, x, y, radius, speed):  # initialize attributes
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.radius = radius  # radius
        self.speed = speed  # speed

    def move_left(self):  # method that moves the point to the left
        self.x -= self.speed  # reducing the x coordinate by the speed of the point

    def move_right(self):  # method that moves the point to the left
        self.x += self.speed  # increasing the x coordinate by the speed of the point

    def move_down(self):  # method that moves the point to the left
        self.y += self.speed  # reducing the y coordinate by the speed of the point

    def move_up(self):  # method that moves the point to the left
        self.y -= self.speed  # increasing they coordinate by the speed of the point


class Game:  # make object game ()
    def __init__(self):  # initialize all attributes (features) of game
        self.point = Point(320, 240, 10, 5)  # put point (character) in game
        self.screen = pygame.display.set_mode((640, 480))  # initialize the screen

    def actions(self):  # define a method to handle game actions
        keys = pygame.key.get_pressed()  # get information about the status of all keyboard keys
        if keys[pygame.K_LEFT]:  # if the left arrow key is pressed
            self.point.move_left()  # call the 'move_left' method of the 'point' object
        if keys[pygame.K_RIGHT]:  # if the right arrow key is pressed
            self.point.move_right()  # Call the 'move_right' method of the 'point' object
        if keys[pygame.K_UP]:  # if the up arrow key is pressed
            self.point.move_up()  # call the 'move_up' method of the 'point' object
        if keys[pygame.K_DOWN]:  # if the down arrow key is pressed
            self.point.move_down()  # call the 'move_down' method of the 'point' object
        # Ensure the point stays within the boundaries of the screen by adjusting its x and y coordinates
        self.point.x = max(self.point.radius, min(640 - self.point.radius, self.point.x))
        self.point.y = max(self.point.radius, min(480 - self.point.radius, self.point.y))

    def rendering(self):  # define a method to render (draw) the game state on the screen
        self.screen.fill((0, 0, 0))  # fill the screen with black color
        # Draw a circle on the screen at the point's position with its radius
        pygame.draw.circle(self.screen, (255, 255, 255), (self.point.x, self.point.y), self.point.radius)
        pygame.display.flip()  # update the screen
        pygame.time.Clock().tick(120)  # Limit the game to n frames per second

    def run(self):  # define the main game loop method
        running = True  # set the game to run
        while running:  # keep running the game loop until 'running' is False
            for event in pygame.event.get():  # process all events in the event queue
                if event.type == pygame.QUIT:  # if the window closure is triggered
                    running = False  # stop the game loop
            self.actions()  # call the 'actions' method to process keyboard inputs
            self.rendering()  # call the 'rendering' method to draw the game state on the screen
        pygame.quit()  # end all pygame modules


game = Game()  # create an instance of the 'Game' class
game.run()  # start the game loop by calling the 'run' method of the game instance
