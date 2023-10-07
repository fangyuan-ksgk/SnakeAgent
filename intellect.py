from agent import *

# This is the Main Function for AI controller
def ai_turn(snake, numbness_level=0.5):
    current_direction = snake.direction    
    directions = snake.get_possible_move()
    
    # Remove the reverse of the current direction to prevent moving backward
    if reverse_map[current_direction] in directions:
        directions.remove(reverse_map[current_direction])
    
    # Choose from the possible directions based on numbness level
    if directions:
        dice = random.random() < numbness_level
        if dice and (current_direction in directions):
            snake.turn(current_direction)
        else:
            rand_direction = random.choice(directions)
            snake.turn(rand_direction)
    else:
        # If no valid directions are left, keep the current direction
        pass
    
    
# Let's try out Spike Neural Net, just to get it outof my head