import pygame
from sys import exit #terminate the program
import os

# Game variables
GAME_WIDTH = 512
GAME_HEIGHT = 512

PLAYER_X = GAME_WIDTH / 2
PLAYER_Y = GAME_HEIGHT / 2
PLAYER_WIDTH = 108
PLAYER_HEIGHT = 108
PLAYER_DISTANCE = 5

#images
background_image = pygame.image.load(os.path.join("images", "temp_background.png")) # load the background image
background_image = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))
player_image_right = pygame.image.load(os.path.join("images", "horse_right.png")) # load the player image
player_image_right = (pygame.transform.scale(player_image_right, (PLAYER_WIDTH, PLAYER_HEIGHT))) # scale the player image to the player's width and height


pygame.init()  # always needed to initialize py game
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("My Game Window") # title of window
pygame.display.set_icon(player_image_right) # set the window icon to the player image
clock = pygame.time.Clock() # to control the frame rate of the game


class Player(pygame.Rect):
    def __init__(self):
        super().__init__(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right

# left (x) and top (y), width and height
player = Player()


def draw():
    # window.fill('blue') # fill the window with blue color
    window.fill((0,0,0)) # fill the window with a custom color using RGB values
    window.blit(background_image, (0,0)) # draw the background image on the window at position (0,80)
    window.blit(player.image, player) # draw the player image on the window at the player's position

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #user clicks the x button in window
            pygame.quit()
            exit()
    
        # KEYDOWN - key was pressed, KEYUP - key was pressed/released
        '''if event.type == pygame.KEYDOWN: # user presses a key
            if event.key in (pygame.K_UP, pygame.K_a): # left arrow key or 'a' key
                player.x -= 10 # move the player left by 10 pixels
            if event.key in (pygame.K_RIGHT, pygame.K_d): # right arrow key or 'd' key
                player.x += 10 # move the player right by 10 pixels
            if event.key in (pygame.K_UP, pygame.K_w): # up arrow key or 'w' key
                player.y -= 10 # move the player up by 10 pixels
            if event.key in (pygame.K_DOWN, pygame.K_s): # down arrow key or 's' key
                player.y += 10 # move the player down by 10 pixels'''

    keys = pygame.key.get_pressed() # get the state of all keyboard buttons
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x = max(player.x - PLAYER_DISTANCE, 0) # move the player left by 5 pixels, but not beyond the left edge of the window 
        
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x = min(player.x + PLAYER_DISTANCE, GAME_WIDTH - player.width) # move the player right by 5 pixels, but not beyond the right edge of the window
        
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y = max(player.y - PLAYER_DISTANCE, 0) # move the player up by 5 pixels, but not above the top of the window

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y = min(player.y + PLAYER_DISTANCE, GAME_HEIGHT - player.height) # move the player down by 5 pixels, but not below the bottom of the window

    draw()
    pygame.display.update()
    clock.tick(60) # set the frame rate to 60 fps