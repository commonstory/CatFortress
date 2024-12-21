class Resources:
    def __init__(self):
        self.wood_capacity = None
        self.wood_count = None
        self.stone_capacity = None
        self.stone_count = None

class Player:
    def __init__(self):
        self.player_health = None
        self.has_pickaxe = None
        self.player_x, self.player_y = 5, 5  # Starting position in grid (5, 5)
        self.player_speed = 1