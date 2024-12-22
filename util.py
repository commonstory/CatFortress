def is_near(player_pos, pos, proximity=1):
    """
    Checks if the player is near the pos.

    Args:
        player_pos: Tuple (x, y) of the player's position in grid coordinates.
        pos: Tuple (x, y) of the  position in grid coordinates.
        proximity: The Manhattan distance to consider "near".

    Returns:
        True if the player is near the pos, False otherwise.
    """
    # dx = abs(player_pos[0] - pos[0])
    # dy = abs(player_pos[1] - pos[1])

    px, py = player_pos
    mx, my = pos
    return abs(px - mx) <= 1 and abs(py - my) <= 1 #dx + dy <= proximity