import pygame
from sys import exit #terminate the program
import os

# Game variables
TILE_SIZE = 32
GAME_WIDTH = 612
GAME_HEIGHT = 612

PLAYER_X = GAME_WIDTH / 2 # x location where the horse spawns when you run the game
PLAYER_Y = GAME_HEIGHT / 2 # y location where the horse spawns when you run the game
PLAYER_WIDTH = 108
PLAYER_HEIGHT = 108
PLAYER_JUMP_WIDTH = 108
PLAYER_JUMP_HEIGHT = 108
PLAYER_DISTANCE = 5

GRAVITY = 0.5
PlAYER_VELOCITY_Y = -10
PLAYER_VELOCITY_X = 5


#images
def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join("images", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

background_image = load_image("temp_background.png", (GAME_WIDTH, GAME_HEIGHT))
player_image_right = load_image("Horse_Right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image("Horse_Left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_right= load_image("Horse_jump_right.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_jump_left= load_image("Horse_jump_left.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
floor_tile_image = load_image("floor-tile2.png", (TILE_SIZE, TILE_SIZE))


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
        if self.jumping:
            # self.width = PLAYER_JUMP_WIDTH
            # self.height = PLAYER_JUMP_HEIGHT
            if self.direction == "right":
                self.image = player_image_jump_right
            elif self.direction == "left":
                self.image = player_image_jump_left
        else:
            # self.width = PLAYER_WIDTH
            # self.height = PLAYER_HEIGHT
            if self.direction == "right":
                self.image = player_image_right
            if self.direction == "left":
                self.image = player_image_left


# left (x) and top (y), width and height
player = Player()

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

def create_map():
    # Floating platform
    for i in range(6):
        tile = Tile(player.x + i * TILE_SIZE, player.y + 2 * TILE_SIZE*2, floor_tile_image)
        tiles.append(tile)

    # Main floor
    for i in range(50): # range to cover more width
        tile = Tile(i*TILE_SIZE, GAME_HEIGHT - TILE_SIZE, floor_tile_image) # Fixed '-' to '='
        tiles.append(tile)

    # Vertical stack/wall
    for i in range(3):
        tile = Tile(TILE_SIZE*3, (i+10)*TILE_SIZE, floor_tile_image)
        tiles.append(tile) 

def check_tile_collision():
    for tile in tiles:
        if player.colliderect(tile):
            return tile
    return None

# def check_tile_collision_x():
#     tile = check_tile_collision()
#     if tile is not None:
#         if player.velocity_x < 0:
#             player.x = tile.x + tile.width
#         elif player.velocity_x > 0:
#             player.x = tile.x - player.width
#         player.velocity_x = 0

# def check_tile_collision_y():
#     tile = check_tile_collision()
#     if tile is not None:
#         if player.velocity_y < 0:
#             player.y = tile.y + tile.height
#         elif player.velocity_y > 0:
#             player.y = tile.y - player.height
#             player.jumping = False
#         player.velocity_y = 0
        

def move_player_x(velocity_x):
    move_map_x(velocity_x)

def move_map_x(velocity_x):
    for tile in tiles:
        tile.x += velocity_x


def move():
    # x movement
    # check_tile_collision_x()


    # y movement
    player.velocity_y += GRAVITY #apply gravity
    player.y += player.velocity_y 

    # check_tile_collision_y()

    # Check for collisions with tiles
    collided_tile = check_tile_collision()
    if collided_tile:
        # If falling downwards
        if player.velocity_y > 0:
            player.y = collided_tile.top - player.height
            player.velocity_y = 0
            player.jumping = False
        # If jumping upwards (hitting head)
        elif player.velocity_y < 0:
            player.y = collided_tile.bottom
            player.velocity_y = 0


def draw():
    # window.fill('blue') # fill the window with blue color
    window.fill((0,0,0)) # fill the window with a custom color using RGB values
    window.blit(background_image, (0,0)) # draw the background image on the window at position (0,80)
    
    for tile in tiles:
        window.blit(tile.image, tile)
    
    player.update_image()
    window.blit(player.image, player) # draw the player image on the window at the player's position


# start game
# player = Player()
tiles= []
create_map()


while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #user clicks the x button in window
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed() # get the state of all keyboard buttons
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        # player.x = max(player.x - PLAYER_DISTANCE, 0) # move the player left by 5 pixels, but not beyond the left edge of the window 
        move_player_x(PLAYER_VELOCITY_X)
        player.direction = "left"

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        # player.x = min(player.x + PLAYER_DISTANCE, GAME_WIDTH - player.width) # move the player right by 5 pixels, but not beyond the right edge of the window
        move_player_x(-PLAYER_VELOCITY_X)
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