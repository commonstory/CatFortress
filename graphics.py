import pygame
from models import Player

# Define constants
WIDTH, HEIGHT = 800, 600   # Window size
TILE_SIZE = 40             # Size of each tile in the grid
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE  # Number of tiles in the window

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Player color
GRASS_COLOR = (34, 139, 34)  # Grass color
STONE_COLOR = (169, 169, 169)  # Stone color
HOUSE_COLOR = (70, 130, 180)  # House color
WORKSHOP_COLOR = (128, 128, 0)  # Workshop color (olive)
STORAGE_COLOR = (255, 215, 0)  # Storage color (gold)
FORT_COLOR = (139, 69, 19)  # Fortification color (brown)
TREE_COLOR = (34, 139, 34)  # Tree color (same as grass for simplicity)
GOBLIN_COLOR = (0, 255, 0)  # Goblin color (green)

def sprite_sheet(size,file,pos):

    #Initial Values
    len_sprt_x,len_sprt_y = size #sprite size
    sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet

    sheet = pygame.image.load(file).convert_alpha() #Load the sheet
    sheet_rect = sheet.get_rect()
    sprites = []
    for i in range(0,sheet_rect.height-len_sprt_y,size[1]):#rows
        for i in range(0,sheet_rect.width-len_sprt_x,size[0]):#columns
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0
    return sprites

# List of collidable tiles
COLLIDABLE_TILES = ["stone", "tree"]

class Graphics:
    def __init__(self, screen):
        self.screen = screen
        # Load the grass sprite
        self.grass_image = pygame.image.load("grass.png")
        self.stone_image = pygame.image.load("stone.png")
        self.tree_image = pygame.image.load("tree.png")
        self.player = sprite_sheet((65, 65), "SaraFullSheet.png", (0, 0))

    # Function to draw the grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            for y in range(0, HEIGHT, TILE_SIZE):
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                # pygame.draw.rect(screen, WHITE, rect, 1)  # Draw grid lines

    # Function to draw the map
    def draw_map(self, game_map):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                tile = game_map[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == "grass":
                    self.screen.blit(self.grass_image, (x * TILE_SIZE, y * TILE_SIZE))
                    # pygame.draw.rect(screen, GRASS_COLOR, rect)  # Draw grass tiles
                elif tile == "stone":
                    self.screen.blit(self.stone_image, (x * TILE_SIZE, y * TILE_SIZE))
                    # pygame.draw.rect(screen, STONE_COLOR, rect)  # Draw stone tiles
                elif tile == "house":
                    pygame.draw.rect(self.screen, HOUSE_COLOR, rect)  # Draw house tiles
                elif tile == "workshop":
                    pygame.draw.rect(self.screen, WORKSHOP_COLOR, rect)  # Draw workshop tiles
                elif tile == "storage":
                    pygame.draw.rect(self.screen, STORAGE_COLOR, rect)  # Draw storage tiles
                elif tile == "fort":
                    pygame.draw.rect(self.screen, FORT_COLOR, rect)  # Draw fort tiles
                elif tile == "tree":
                    self.screen.blit(self.tree_image, (x * TILE_SIZE, y * TILE_SIZE))

    def draw_player(self, player_pos):
        self.screen.blit(self.player[40], (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE - 30))

    # Function to draw the goblins
    def draw_goblins(self, goblins):
        for goblin in goblins:
            goblin_rect = pygame.Rect(goblin['x'] * TILE_SIZE, goblin['y'] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(self.screen, GOBLIN_COLOR, goblin_rect)  # Draw goblins as green squares

    # Function to draw the player's resource (stone and wood count)
    def draw_resources(self, player:Player):
        font = pygame.font.SysFont("Arial", 24)
        resource_text = font.render(f"Stone: {player.stone_count}/{player.stone_capacity}  Wood: {player.wood_count}/{player.wood_capacity}  Pickaxe: {'Yes' if player.has_pickaxe else 'No'}  Health: {player.player_health}", True, WHITE)
        self.screen.blit(resource_text, (10, 10))  # Draw resources at the top-left corner
