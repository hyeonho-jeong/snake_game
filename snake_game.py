import pygame
import os
import sys
import random
import time

# origian game window set
hj_win_posx = 700
hj_win_posy = 300
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (hj_win_posx, hj_win_posy)

# window setting

hj_WINDOW_WIDTH = 540
hj_WINDOW_HEIGHT = 600
hj_GRID = 30
hj_GRID_WIDTH = int(hj_WINDOW_WIDTH/hj_GRID)
hj_GRID_HEIGHT = int(hj_WINDOW_HEIGHT/hj_GRID)

# color setting

hj_BLACK = 0, 0, 0
hj_WHITE = 255,255,255
hj_RED = 255, 0, 0
hj_GREEN1 = 25, 102, 25
hj_GREEN2 = 51, 204, 51
hj_GREEN3 = 233, 249, 185
hj_BLUE = 17, 17, 212
hj_LIGHT_PINK1 = 255, 230, 255
hj_LIGHT_PINK2 = 255, 204, 255

hj_NORTH = ( 0, -1)
hj_SOUTH = ( 0,  1)
hj_WEST  = (-1,  0)
hj_EAST  = ( 1,  0)

def main():
    y=input("What is your name?: ")
    print(f"welcome to play the snake game {y}")


class Snake:

    def __init__(self):
        self.length = 1
        self.create_snake()
        self.color1 = hj_GREEN2
        self.color2 = hj_GREEN3
        self.head_color = hj_GREEN1

    def create_snake(self):
        self.length = 3
        self.positions = [(int(hj_WINDOW_WIDTH/2), int(hj_WINDOW_HEIGHT/2))]
        self.direction = random.choice([hj_NORTH, hj_SOUTH, hj_WEST, hj_EAST])
        global game_score
        game_score = 0

    def move_snake(self, surface):

        # print(len(self.positions))
        head = self.get_head_position()
        x, y = self.direction
        next = ((head[0] + (x*hj_GRID)) % hj_WINDOW_WIDTH, (head[1] + (y*hj_GRID)) % hj_WINDOW_HEIGHT)
        if next in self.positions[2:]:
            self.create_snake()
            gameover(surface)
        else:
            self.positions.insert(0, next)
            if len(self.positions) > self.length:
                del self.positions[-1]

    def draw_snake(self, surface):
        for index, pos in enumerate(self.positions):
            if index == 0:
                draw_object(surface, self.head_color, pos)
            elif index % 2 == 0:
                draw_object(surface, self.color1, pos)
            else:
                draw_object(surface, self.color2, pos)


    def game_control(self, arrowkey):
        if (arrowkey[0]*-1, arrowkey[1]*-1) == self.direction:
            return
        else:
            self.direction = arrowkey

    def get_head_position(self):
        return self.positions[0]

        # food's class

class Food:
    def __init__(self):
        self.position =(0, 0)
        self.color = hj_RED
        self.randomize_food()

    def randomize_food(self):
        self.position = (random.randint(0, hj_GRID_WIDTH-1) * hj_GRID,
                        random.randint(0, hj_GRID_HEIGHT-1) * hj_GRID)

    def draw_food(self, surface):
        draw_object(surface, self.color, self.position)

def eating_food(x):
    return x + 1

        # game detail


def draw_background(surface):
    background = pygame.Rect((0,0),(hj_WINDOW_WIDTH, hj_WINDOW_HEIGHT))
    pygame.draw.rect(surface, hj_WHITE, background)
    draw_grid(surface)

def draw_grid(surface):
    for row in range(0,int(hj_GRID_HEIGHT)):
        for col in range(0, int(hj_GRID_WIDTH)):
            if (row+col) % 2 == 0:
                rect = pygame.Rect((col*hj_GRID, row*hj_GRID), (hj_GRID, hj_GRID))
                pygame.draw.rect(surface, hj_LIGHT_PINK1, rect)
            else:
                rect = pygame.Rect((col*hj_GRID, row*hj_GRID), (hj_GRID, hj_GRID))
                pygame.draw.rect(surface, hj_LIGHT_PINK2, rect)


def draw_object(surface, color, pos):
    rect = pygame.Rect((pos[0], pos[1]), (hj_GRID,hj_GRID))
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, hj_WHITE, rect, 1)

def screen_area_of_rectangle(width, height):
    area = width*height
    return area

def position_check(snake, food_group):
    for food in food_group:
        if snake.get_head_position() == food.position:
            global game_score
            game_score += 1
            snake.length += 1
            food.randomize_food()


def show_info(surface, snake, speed):
    font = pygame.font.SysFont('malgungothic',35)
    image = font.render(f" snake's length: {snake.length} LV: {int(speed//2)} ", True, hj_BLUE)
    pos = image.get_rect()
    pos.move_ip(20,20)
    pygame.draw.rect(image, hj_BLACK,(pos.x-20, pos.y-20, pos.width, pos.height), 2)
    surface.blit(image, pos)

def gameover(surface):
    font = pygame.font.SysFont('malgungothic',50)
    image = font.render('GAME OVER', True, hj_BLACK)
    pos = image.get_rect()
    pos.move_ip(120,220)
    surface.blit(image, pos)
    pygame.display.update()
    time.sleep(2)

player = Snake()
run = True
game_score = 0


        # food

def draw_food_group(food_group, surface):
    for food in food_group:
        food.draw_food(surface)

food = Food()
food_group = []

for i in range(3):
    food = Food()
    food_group.append(food)

for food in food_group:
    print(food.position)

        # game loop

pygame.init()
pygame.display.set_caption('SNAKE GAME')
screen = pygame.display.set_mode((hj_WINDOW_WIDTH, hj_WINDOW_HEIGHT))
clock = pygame.time.Clock()

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            if event.key == pygame.K_UP:
                player.game_control(hj_NORTH)
            if event.key == pygame.K_DOWN:
                player.game_control(hj_SOUTH)
            if event.key == pygame.K_RIGHT:
                player.game_control(hj_EAST)
            if event.key == pygame.K_LEFT:
                player.game_control(hj_WEST)

    draw_background(screen)
    player.move_snake(screen)
    position_check(player, food_group)
    player.draw_snake(screen)
    draw_food_group(food_group, screen)
            # food.draw_food(screen)
    speed = player.length/2
    show_info(screen, player, speed)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(5+speed)


        # pygame closed
    
if __name__ == "__main__":
    main()

    print('pygame closed')
    pygame.quit()
    sys.exit()
