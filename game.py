import sys
import random
from graphics import *
from models import Player

# Initialize Pygame
pygame.init()
# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
graphics = Graphics(screen)
pygame.display.set_caption('Cats Fortress Game')

# Player properties
player = Player()
player.player_x, player.player_y = 5, 5  # Starting position in grid (5, 5)
player.player_speed = 1            # Speed of player movement
player.has_pickaxe = False         # Whether the player has crafted a pickaxe
player.player_health = 100         # Player health
player.stone_count = 0             # Stone collected by the player
player.wood_count = 0              # Wood collected by the player
player.stone_capacity = 50         # Max stone the player can carry
player.wood_capacity = 50          # Max wood the player can carry

# Enemy properties
goblins = []                # List of goblin enemies
goblin_count = 3            # Number of goblins to spawn
goblin_speed = 0.5          # Goblin movement speed

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

# Function to handle mining
def mine_tile(game_map, x, y):
    if game_map[y][x] == "stone" and player.stone_count < player.stone_capacity:
        game_map[y][x] = "grass"  # Mine the stone by turning it into grass
        player.stone_count += 1  # Increase the stone count
        if player.has_pickaxe:
            player.stone_count += 1  # Pickaxe mines 2 stones at once

# Function to handle cutting trees
def cut_tree(game_map, x, y):
    if game_map[y][x] == "tree" and player.wood_count < player.wood_capacity:
        game_map[y][x] = "grass"  # Cut down the tree by turning it into grass
        player.wood_count += 1  # Increase the wood count

# Function to handle building placement
def place_building(game_map, x, y):
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
        if player.stone_count >= building_costs["house"]["stone"] and player.wood_count >= building_costs["house"]["wood"]:
            game_map[y][x] = "house"
            player.stone_count -= building_costs["house"]["stone"]
            player.wood_count -= building_costs["house"]["wood"]
        elif player.stone_count >= building_costs["workshop"]["stone"] and player.wood_count >= building_costs["workshop"]["wood"]:
            game_map[y][x] = "workshop"
            player.stone_count -= building_costs["workshop"]["stone"]
            player.wood_count -= building_costs["workshop"]["wood"]
        elif player.stone_count >= building_costs["storage"]["stone"] and player.wood_count >= building_costs["storage"]["wood"]:
            game_map[y][x] = "storage"
            player.stone_count -= building_costs["storage"]["stone"]
            player.wood_count -= building_costs["storage"]["wood"]
        elif player.stone_count >= building_costs["fort"]["stone"] and player.wood_count >= building_costs["fort"]["wood"]:
            game_map[y][x] = "fort"
            player.stone_count -= building_costs["fort"]["stone"]
            player.wood_count -= building_costs["fort"]["wood"]

# Function to craft the pickaxe in the workshop
def craft_pickaxe(game_map, x, y):
    if game_map[y][x] == "workshop" and player.stone_count >= 5 and player.wood_count >= 3 and not player.has_pickaxe:
        player.stone_count -= 5
        player.wood_count -= 3
        player.has_pickaxe = True  # The player now has a pickaxe
        print("Pickaxe crafted!")

# Function to move goblins
def move_goblins():
    for goblin in goblins:
        # Goblins will move towards the player
        if goblin['x'] < player.player_x:
            goblin['x'] += goblin_speed
        elif goblin['x'] > player.player_x:
            goblin['x'] -= goblin_speed
        if goblin['y'] < player.player_y:
            goblin['y'] += goblin_speed
        elif goblin['y'] > player.player_y:
            goblin['y'] -= goblin_speed

# Function to handle combat
def check_combat():
    for goblin in goblins:
        if goblin['x'] == player.player_x and goblin['y'] == player.player_y:
            # Player loses health when touched by a goblin
            player.player_health -= 10
            print(f"Player health: {player.player_health}")
            # Goblin drops resources when defeated
            player.stone_count += 5
            player.wood_count += 3
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
        player_pos = (player.player_x, player.player_y)
        # Draw the map
        graphics.draw_map(game_map)
        highlight_nearby_collidable_tiles(player_pos, game_map)  # Highlight nearby collidable tiles
        # Draw the grid
        graphics.draw_grid()

        # Draw the player
        graphics.draw_player(player_pos)

        # Draw the goblins
        graphics.draw_goblins(goblins)

        # Draw the resources and health
        graphics.draw_resources(player)

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

        player.player_x,player.player_y = move_player(dx, dy, player_pos, game_map)
        # Move goblins and check for combat
        move_goblins()
        check_combat()

        # Update the screen
        pygame.display.flip()
        clock.tick(10)  # Limit the frame rate to 60 FPS

# Run the game
if __name__ == "__main__":
    main()
