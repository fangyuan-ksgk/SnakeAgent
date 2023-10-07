import pygame, sys, time, random

def close_pos(p1, p2):
    # print('Pos 1': p1, ' Pos 2': p2)
    is_close =  abs(p1[0]-p2[0])<10 and abs(p1[1]-p2[1])<10
    # print('close? ', is_close)
    return is_close

def decide_speed_from_size(size):
    speed = 5 + (size + 3)//5
    speed = min(speed, 15)
    return speed

reverse_map = {'UP':'DOWN',
               'DOWN':'UP',
               'LEFT':'RIGHT',
               'RIGHT':'LEFT'}

class Snake:
    def __init__(self, initial_pos, color, frame_x, frame_y):
        self.body = [initial_pos, [initial_pos[0]-10, initial_pos[1]], [initial_pos[0]-(2*10), initial_pos[1]]]
        self.direction = 'RIGHT'
        self.color = color
        self.alive = True
        self.speed = decide_speed_from_size(len(self.body))
        self.unit_mass = self.speed * self.speed
        self.food_in_store = 0.
        self.frame_x = frame_x
        self.frame_y = frame_y


    def valid_pos(self, x, y):
        if x < 0 or x >= self.frame_x or y < 0 or y >= self.frame_y:
            return False
        else:
            return True

    def check_alive(self):
        if len(self.body) == 0:
            self.alive = False
            return self.alive
        # check inside frame
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= self.frame_x or head_y < 0 or head_y >= self.frame_y:
            self.alive = False
        return self.alive

    def get_possible_move(self):
        directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
        poss_directions = []
        move_map = {'UP': (0,-10), 'DOWN': (0,10), 'LEFT':(-10,0), 'RIGHT':(10,0)}
        for d in directions:
            n_x = self.body[0][0] + move_map[d][0]
            n_y = self.body[0][1] + move_map[d][1]
            if 0 <= n_x <= self.frame_x and 0 <= n_y <= self.frame_y:
                poss_directions.append(d)
        return poss_directions


    def move(self):
        # movement speed is proportional to body size
        self.speed = decide_speed_from_size(len(self.body))
        self.unit_mass = self.speed * self.speed
        
        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            head_y -= self.speed
        elif self.direction == 'DOWN':
            head_y += self.speed
        elif self.direction == 'LEFT':
            head_x -= self.speed
        elif self.direction == 'RIGHT':
            head_x += self.speed
        self.body.insert(0, [head_x, head_y])
        # Automatically Grow when there are foods in its stomach
        # Food can only grow snake's mass
        if self.food_in_store>=self.unit_mass:
            self.food_in_store -= self.unit_mass
        else:
            self.body.pop()
    
 
    def sign(self, x):
        return (x > 0) - (x < 0)
        
    def infer_move(self, direc):
        dx, dy = direc
        if dx>0 and dy==0:
            return 'RIGHT'
        if dx<0 and dy==0:
            return 'LEFT'
        if dy>0 and dx==0:
            return 'DOWN'
        if dy<0 and dx==0:
            return 'UP'

    # This is used to update direction
    def turn(self, direction):
        if self.direction != reverse_map[direction]:
            # Only turn when possible
            self.direction = direction
    
    def eat(self, food_pos=None, other_snakes=[]):
    
        if len(self.body)==0:
            return False
        if food_pos != None:
            if close_pos(self.body[0], food_pos):
            # if self.body[0] == food_pos:
                self.food_in_store += 10*10
                return 'food'
        # a dot doesn't get to eat anyone else, only food
        if len(self.body)==1:
            return False
        for other_snake in other_snakes:
            if not other_snake.alive:
                continue
            if len(other_snake.body)==0:
                other_snake.alive = False
                continue
            # print('other snakes: ', type(other_snakes))
            # print('other_snake: ', type(other_snake))
            if any(close_pos(self.body[0], p) for p in other_snake.body):
            # if self.body[0] in other_snake.body:
                # print(f"Snake at {self.body[0]} checking for food or other snakes...")
                # Determine the number of segments to bite off
                bite_mass = len(self.body)*self.unit_mass/2
                have_mass = len(other_snake.body)*other_snake.unit_mass
                # bite_size = len(self.body)//2
                # have_size = len(other_snake.body)
                print('Original Food Storage at: ', self.food_in_store)
                if have_mass <= bite_mass:
                    other_snake.get_eaten(int(have_mass)//other_snake.unit_mass)
                    other_snake.alive = False
                    self.food_in_store += have_mass
                    print(f'Biting off {have_mass} from another snake, kill it')
                    print('Own Food Storage at: ', self.food_in_store)
                else:
                    other_snake.get_eaten(int(bite_mass)//other_snake.unit_mass)
                    self.food_in_store += bite_mass
                    print(f'Biting off {bite_mass} from another snake, leave it')
                    print('Own Food Storage at: ', self.food_in_store)
                return 'snake'
        return False
    

    def get_eaten(self, n=3):
        # Remove the last n segments of the snake's body
        for _ in range(n):
            if len(self.body) >= 1:  # Ensure the snake's length doesn't go below 1
                self.body.pop()

    def grow_one_unit(self):

        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            head_y -= 10
        elif self.direction == 'DOWN':
            head_y += 10
        elif self.direction == 'LEFT':
            head_x -= 10
        elif self.direction == 'RIGHT':
            head_x += 10
        self.body.insert(0, [head_x, head_y]) 
        
        
# Food Class 
class Food:
    def __init__(self, snake_body, frame_size_x, frame_size_y):
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.position = self.generate_food(snake_body)
        self.mass = 10*10.
    def generate_food(self, occupied_positions):
        while True:
            x = random.randrange(1, (self.frame_size_x//10)) * 10
            y = random.randrange(1, (self.frame_size_y//10)) * 10
            if [x, y] not in occupied_positions:
                return [x, y]
            
            
def is_snake_dead(snake):
    head_x, head_y = snake.body[0]
    # Check if the snake is out of bounds
    if head_x < 0 or head_x >= frame_size_x or head_y < 0 or head_y >= frame_size_y:
        return True
    # Check if the snake has collided with itself
    if snake.body[0] in snake.body[1:]:
        return True
    return False
