"""
Snake Eater
with lots of Snake
Made with PyGame
"""

import pygame, sys, time, random
from object import *

difficulty = 10

# Window size
frame_size_x = int(720*2)
frame_size_y = int(480*2)

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()
           

# Game Terminate -- with option to restart with buttom 1
def game_terminate():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False


# Score
score = 0

def show_score():
    score_font = pygame.font.SysFont('consolas', 20)
    score_surface = score_font.render('Score : ' + str(score), True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (frame_size_x/10, 15)
    game_window.blit(score_surface, score_rect)


# Main loop

# Initialize the snake and food
player_snake = Snake([100, 50], green, frame_size_x, frame_size_y)
# add AI snake which moves at random, and can be eaten, if its body is touched by
# another snake's head.
num_ai = 20
num_food = 3
ai_snakes = [Snake([random.randint(0, frame_size_x-10)//10*10, random.randint(0, frame_size_y-10)//10*10], red, frame_size_x, frame_size_y) for _ in range(num_ai)]

pos_occupied = player_snake.body + [ai_snake.body for ai_snake in ai_snakes]
foods = [Food(pos_occupied, frame_size_x, frame_size_y) for _ in range(num_food)]

# Main loop
# Matter keeps the same amount ! 
running = True
while running:
    game_window.fill(black)  # Clear the screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                if player_snake.direction != 'DOWN':
                    player_snake.direction = 'UP'
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                if player_snake.direction != 'UP':
                    player_snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT or event.key == ord('a'):
                if player_snake.direction != 'RIGHT':
                    player_snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                if player_snake.direction != 'LEFT':
                    player_snake.direction = 'RIGHT'
            elif event.key == pygame.K_ESCAPE:
                running = False


    # Move the snake
    player_snake.move()

    # Move the AI snakes and check if they are alive
    for ai_snake in ai_snakes:
        ai_turn(ai_snake, numbness_level=0.8)  # Adjust numbness_level as needed
        ai_snake.move()

    # Check whether Player & AI snake eats food, or each other

    # Player Snake eats food
    for food in foods:
        eat_result = player_snake.eat(food.position, [])
        if eat_result == 'food':
            foods.remove(food)
            new_food = Food(player_snake.body + [ai_snake.body for ai_snake in ai_snakes], frame_size_x, frame_size_y)
            foods.append(new_food)

    # Player & AI Snakes eat each other
    # print('Player head: ', player_snake.body[0])
    # print('Ai body: ', ai_snakes[0].body)
    player_snake.eat(None, ai_snakes)
    
    
    for i in range(len(ai_snakes)):
        ai_snakes[i].eat(None, ai_snakes[:i]+ai_snakes[i+1:])
        ai_snakes[i].eat(None, [player_snake])
        
    
            
    # Check Aliveness and Respawn AI snake
    dead_ai_snakes = []
    for ai in ai_snakes:
        if not ai.check_alive():
            dead_ai_snakes.append(ai)
    for dead_snake in dead_ai_snakes:
        print("A snake died. Respawning...")
        ai_snakes.remove(dead_snake)
        
        # Choose a corner for respawn: left-top or right-top
        corner_choice = random.choice(['left-top', 'right-top'])

        if corner_choice == 'left-top':
            new_ai_snake = Snake([0, 0], red, frame_size_x, frame_size_y)
        else:  # right-top
            new_ai_snake = Snake([frame_size_x - 10, 0], red, frame_size_x, frame_size_y)
        
        ai_snakes.append(new_ai_snake)
    
    # Draw the player snake
    for segment in player_snake.body:
        pygame.draw.rect(game_window, player_snake.color, pygame.Rect(segment[0], segment[1], max(player_snake.speed,10), max(player_snake.speed,10)))

    # Draw all AI snakes
    for ai_snake in ai_snakes:
        for segment in ai_snake.body:
            pygame.draw.rect(game_window, ai_snake.color, pygame.Rect(segment[0], segment[1], max(10,ai_snake.speed), max(10,ai_snake.speed)))

    # Draw all food items
    for food in foods:
        pygame.draw.rect(game_window, white, pygame.Rect(food.position[0], food.position[1], 10, 10))


    # Display the score
    show_score()

    # Check for game over conditions for player snake
    if len(player_snake.body)==0 or not player_snake.alive:
        print("Player got Bitten and Die")
        if game_terminate():  # If player presses '1' to restart
            player_snake = Snake([100, 50], green, frame_size_x, frame_size_y)
            food = Food(player_snake.body, frame_size_x, frame_size_y)
            score = 0
        else:
            pygame.quit()
            sys.exit()
    elif player_snake.body[0][0] < 0 or player_snake.body[0][0] > frame_size_x-10:
        print("Player snake went out of bounds horizontally.")
        if game_terminate():  # If player presses '1' to restart
            player_snake = Snake([100, 50], green, frame_size_x, frame_size_y)
            food = Food(player_snake.body, frame_size_x, frame_size_y)
            score = 0
        else:
            pygame.quit()
            sys.exit()
    elif player_snake.body[0][1] < 0 or player_snake.body[0][1] > frame_size_y-10:
        print("Player snake went out of bounds vertically.")
        if game_terminate():  # If player presses '1' to restart
            player_snake = Snake([100, 50], green, frame_size_x, frame_size_y)
            food = Food(player_snake.body, frame_size_x, frame_size_y)
            score = 0
        else:
            pygame.quit()
            sys.exit()
    # elif player_snake.body[0] in player_snake.body[1:]:
    #     print("Player snake collided with itself.")
    #     # if game_terminate():  # If player presses '1' to restart
    #         # player_snake = Snake([100, 50], green)
    #         # food = Food(player_snake.body)
    #         # score = 0
    #     else:
    #         pygame.quit()
    #         sys.exit()

    pygame.display.flip()  # Update the display
    fps_controller.tick(difficulty)  # Control the game speed

pygame.quit()

