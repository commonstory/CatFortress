import pygame
import sys
import random

# Initialize Pygame
pygame.init()

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

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dwarf Fortress-like Game')

# Player properties
player_x, player_y = 5, 5  # Starting position in grid (5, 5)
player_speed = 1            # Speed of player movement
stone_count = 0             # Stone collected by the player
wood_count = 0              # Wood collected by the player
stone_capacity = 50         # Max stone the player can carry
wood_capacity = 50          # Max wood the player can carry
has_pickaxe = False         # Whether the player has crafted a pickaxe
player_health = 100         # Player health

# Enemy properties
goblins = []                # List of goblin enemies
goblin_count = 3            # Number of goblins to spawn
goblin_speed = 0.5          # Goblin movement speed

# Load the grass sprite
grass_image = pygame.image.load("grass.png")
stone_image = pygame.image.load("stone.png")

# List of collidable tiles
COLLIDABLE_TILES = ["stone", "tree"]

def is_collision(next_x, next_y, game_map):
    """
    Check if the next position is a collidable tile.
    next_x, next_y: The player's next grid position
    game_map: The 2D array of the map
    Returns True if the tile is collidable, False otherwise
    """
    if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT:
        tile = game_map[next_y][next_x]
        return tile in COLLIDABLE_TILES
    return True  # Out-of-bounds positions are treated as collidable


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

player = sprite_sheet((65,65),"SaraFullSheet.png",(0,0))

# Map generation function
def generate_map():
    game_map = []
    for y in range(GRID_HEIGHT):
        row = []
        for x in range(GRID_WIDTH):
            # Randomly decide whether the tile is grass, stone, or a tree
            rand = random.random()
            if rand < 0.7:  # 70% chance for grass
                row.append("grass")
            elif rand < 0.85:  # 15% chance for stone
                row.append("stone")
            else:  # 15% chance for tree
                row.append("tree")
        game_map.append(row)
    return game_map

# Function to draw the grid
def draw_grid():
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            #pygame.draw.rect(screen, WHITE, rect, 1)  # Draw grid lines

# Function to draw the map
def draw_map(game_map):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = game_map[y][x]
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == "grass":
                screen.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
                #pygame.draw.rect(screen, GRASS_COLOR, rect)  # Draw grass tiles
            elif tile == "stone":
                screen.blit(stone_image, (x * TILE_SIZE, y * TILE_SIZE))
                #pygame.draw.rect(screen, STONE_COLOR, rect)  # Draw stone tiles
            elif tile == "house":
                pygame.draw.rect(screen, HOUSE_COLOR, rect)  # Draw house tiles
            elif tile == "workshop":
                pygame.draw.rect(screen, WORKSHOP_COLOR, rect)  # Draw workshop tiles
            elif tile == "storage":
                pygame.draw.rect(screen, STORAGE_COLOR, rect)  # Draw storage tiles
            elif tile == "fort":
                pygame.draw.rect(screen, FORT_COLOR, rect)  # Draw fort tiles
            elif tile == "tree":
                pygame.draw.rect(screen, TREE_COLOR, rect)  # Draw tree tiles
def draw_player():
    #player_rect = pygame.Rect(player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    #pygame.draw.rect(screen, RED, player_rect)  # Draw the player as a red square

    screen.blit(player[40], (player_x * TILE_SIZE, player_y * TILE_SIZE -30))

# Function to draw the goblins
def draw_goblins():
    for goblin in goblins:
        goblin_rect = pygame.Rect(goblin['x'] * TILE_SIZE, goblin['y'] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, GOBLIN_COLOR, goblin_rect)  # Draw goblins as green squares

# Function to handle mining
def mine_tile(game_map, x, y):
    global stone_count
    if game_map[y][x] == "stone" and stone_count < stone_capacity:
        game_map[y][x] = "grass"  # Mine the stone by turning it into grass
        stone_count += 1  # Increase the stone count
        if has_pickaxe:
            stone_count += 1  # Pickaxe mines 2 stones at once

# Function to handle cutting trees
def cut_tree(game_map, x, y):
    global wood_count
    if game_map[y][x] == "tree" and wood_count < wood_capacity:
        game_map[y][x] = "grass"  # Cut down the tree by turning it into grass
        wood_count += 1  # Increase the wood count

# Function to handle building placement
def place_building(game_map, x, y):
    global stone_count, wood_count, has_pickaxe
    # Cost of each building type
    building_costs = {
        "house": {"stone": 5, "wood": 0},
        "workshop": {"stone": 10, "wood": 5},
        "storage": {"stone": 8, "wood": 4},
        "fort": {"stone": 15, "wood": 10},
    }

    # Check if enough resources are available
    if game_map[y][x] == "grass":
        # Check if player has enough resources for each building type
        if stone_count >= building_costs["house"]["stone"] and wood_count >= building_costs["house"]["wood"]:
            game_map[y][x] = "house"
            stone_count -= building_costs["house"]["stone"]
            wood_count -= building_costs["house"]["wood"]
        elif stone_count >= building_costs["workshop"]["stone"] and wood_count >= building_costs["workshop"]["wood"]:
            game_map[y][x] = "workshop"
            stone_count -= building_costs["workshop"]["stone"]
            wood_count -= building_costs["workshop"]["wood"]
        elif stone_count >= building_costs["storage"]["stone"] and wood_count >= building_costs["storage"]["wood"]:
            game_map[y][x] = "storage"
            stone_count -= building_costs["storage"]["stone"]
            wood_count -= building_costs["storage"]["wood"]
        elif stone_count >= building_costs["fort"]["stone"] and wood_count >= building_costs["fort"]["wood"]:
            game_map[y][x] = "fort"
            stone_count -= building_costs["fort"]["stone"]
            wood_count -= building_costs["fort"]["wood"]

# Function to craft the pickaxe in the workshop
def craft_pickaxe(game_map, x, y):
    global stone_count, wood_count, has_pickaxe
    if game_map[y][x] == "workshop" and stone_count >= 5 and wood_count >= 3 and not has_pickaxe:
        stone_count -= 5
        wood_count -= 3
        has_pickaxe = True  # The player now has a pickaxe
        print("Pickaxe crafted!")

# Function to draw the player's resource (stone and wood count)
def draw_resources():
    font = pygame.font.SysFont("Arial", 24)
    resource_text = font.render(f"Stone: {stone_count}/{stone_capacity}  Wood: {wood_count}/{wood_capacity}  Pickaxe: {'Yes' if has_pickaxe else 'No'}  Health: {player_health}", True, WHITE)
    screen.blit(resource_text, (10, 10))  # Draw resources at the top-left corner

# Function to move goblins
def move_goblins():
    global player_x, player_y
    for goblin in goblins:
        # Goblins will move towards the player
        if goblin['x'] < player_x:
            goblin['x'] += goblin_speed
        elif goblin['x'] > player_x:
            goblin['x'] -= goblin_speed
        if goblin['y'] < player_y:
            goblin['y'] += goblin_speed
        elif goblin['y'] > player_y:
            goblin['y'] -= goblin_speed

# Function to handle combat
def check_combat():
    global player_health, stone_count, wood_count
    for goblin in goblins:
        if goblin['x'] == player_x and goblin['y'] == player_y:
            # Player loses health when touched by a goblin
            player_health -= 10
            print(f"Player health: {player_health}")
            # Goblin drops resources when defeated
            stone_count += 5
            wood_count += 3
            goblins.remove(goblin)  # Remove the goblin after it is defeated

def move_player(dx, dy, player_pos, game_map):
    """
    Move the player if there's no collision.
    dx, dy: Change in x and y direction (e.g., dx=1, dy=0 for right movement)
    player_pos: The current position of the player as (x, y)
    game_map: The 2D array of the map
    Returns the updated player position
    """
    next_x = player_pos[0] + dx
    next_y = player_pos[1] + dy

    if not is_collision(next_x, next_y, game_map):
        return next_x, next_y  # Update position if no collision
    return player_pos  # Stay in place if collision occurs

def highlight_nearby_collidable_tiles(player_pos, game_map, rng=1):
    """
    Highlight collidable tiles near the player.
    player_pos: The player's current position (x, y)
    game_map: The 2D array of the map
    range: The distance within which to check for collidable tiles
    """
    px, py = player_pos

    for dy in range(-rng, rng + 1):
        for dx in range(-rng, rng + 1):
            nx, ny = px + dx, py + dy

            # Check if position is within bounds and is collidable
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                if game_map[ny][nx] in COLLIDABLE_TILES:
                    # Draw a translucent overlay on the collidable tile
                    highlight_color = (255, 0, 0, 100)  # Red with transparency
                    highlight_rect = pygame.Rect(
                        nx * TILE_SIZE, ny * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    )
                    highlight_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill(highlight_color)
                    screen.blit(highlight_surface, highlight_rect)


# Main game loop
def main():
    global player_x, player_y
    # Generate the map
    game_map = generate_map()

    # Spawn goblins at random positions
    for _ in range(goblin_count):
        goblin_x = random.randint(0, GRID_WIDTH - 1)
        goblin_y = random.randint(0, GRID_HEIGHT - 1)
        goblins.append({'x': goblin_x, 'y': goblin_y})

    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)  # Fill the screen with black
        player_pos = (player_x, player_y)
        # Draw the map
        draw_map(game_map)
        highlight_nearby_collidable_tiles(player_pos, game_map)  # Highlight nearby collidable tiles
        # Draw the grid
        draw_grid()

        # Draw the player
        draw_player()

        # Draw the goblins
        draw_goblins()

        # Draw the resources and health
        draw_resources()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle right-click to place a building
                if event.button == 3:  # Right-click
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // TILE_SIZE
                    grid_y = mouse_y // TILE_SIZE
                    place_building(game_map, grid_x, grid_y)
                # Handle left-click to gather resources (mine or cut trees)
                elif event.button == 1:  # Left-click
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // TILE_SIZE
                    grid_y = mouse_y // TILE_SIZE
                    if game_map[grid_y][grid_x] == "stone":
                        mine_tile(game_map, grid_x, grid_y)
                    elif game_map[grid_y][grid_x] == "tree":
                        cut_tree(game_map, grid_x, grid_y)

        # Crafting the pickaxe (press "C" when standing on a workshop)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:  # "C" key to craft pickaxe
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // TILE_SIZE
            grid_y = mouse_y // TILE_SIZE
            craft_pickaxe(game_map, grid_x, grid_y)

        # Player movement (arrow keys)
        dx, dy = 0, 0

        if keys[pygame.K_UP]:
            dx, dy = 0, -1
        elif keys[pygame.K_DOWN]:
            dx, dy = 0, 1
        elif keys[pygame.K_LEFT]:
            dx, dy = -1, 0
        elif keys[pygame.K_RIGHT]:
            dx, dy = 1, 0

        player_x,player_y = move_player(dx, dy, player_pos, game_map)
        # Move goblins and check for combat
        move_goblins()
        check_combat()

        # Update the screen
        pygame.display.flip()
        clock.tick(10)  # Limit the frame rate to 60 FPS

# Run the game
if __name__ == "__main__":
    main()
