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
PLAYER_JUMP_WIDTH = 52
PLAYER_JUMP_HEIGHT = 60
PLAYER_DISTANCE = 5

GRAVITY = 0.5
PlAYER_VELOCITY_Y = -10
FLOOR_Y = GAME_HEIGHT * 3/4

#images
def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join("images", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

background_image = load_image("temp_background.png", (GAME_WIDTH, GAME_HEIGHT))
player_image_right = load_image("Horse_Right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image("Horse_Left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))


pygame.init()  # always needed to initialize py game
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("My Game Window") # title of window
pygame.display.set_icon(player_image_right) # set the window icon to the player image
clock = pygame.time.Clock() # to control the frame rate of the game


class Player(pygame.Rect):
    def __init__(self):
        super().__init__(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.velocity_y = 0
        self.direction = "right"
        self.jumping = False

    def update_image(self):
        if self.direction == "right":
            self.image = player_image_right
        if self.direction == "left":
            self.image = player_image_left


# left (x) and top (y), width and height
player = Player()

def move():
    player.y += player.velocity_y # update the player's vertical position based on its velocity
    player.velocity_y += GRAVITY # apply gravity to the player's vertical velocity

    if player.y + player.height > FLOOR_Y:
        player.y = FLOOR_Y - player.height
        player.velocity_y = 0 # Stops falling when hit the floor
        player.jumping = False


def draw():
    # window.fill('blue') # fill the window with blue color
    window.fill((0,0,0)) # fill the window with a custom color using RGB values
    window.blit(background_image, (0,0)) # draw the background image on the window at position (0,80)
    player.update_image()
    window.blit(player.image, player) # draw the player image on the window at the player's position

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #user clicks the x button in window
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed() # get the state of all keyboard buttons
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x = max(player.x - PLAYER_DISTANCE, 0) # move the player left by 5 pixels, but not beyond the left edge of the window 
        player.direction = "left"

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x = min(player.x + PLAYER_DISTANCE, GAME_WIDTH - player.width) # move the player right by 5 pixels, but not beyond the right edge of the window
        player.direction = "right"

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
        player.velocity_y = PlAYER_VELOCITY_Y # set the player's vertical velocity to the defined value (jumping)
        player.jumping = True

    # if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    #     player.y = min(player.y + PLAYER_DISTANCE, GAME_HEIGHT - player.height) # move the player down by 5 pixels, but not below the bottom of the window

    move()

    draw()
    pygame.display.update()
    clock.tick(60) # set the frame rate to 60 fps