from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from numpy import sqrt

init()

# Initializing game parameters

speed = 10  # Game speed

width = 600  # Window width
height = 600  # Window height
cols = 50  # Columns in in window
rows = 50  # Rows in in window
wr = width/cols  # Cell width
hr = height/rows  # Cell height

direction = 1

screen = display.set_mode([width, height])
display.set_caption("HUNGRY NIGEL")
clock = time.Clock()


def getpath(food1, snake1):
    food1.cameFrom = []
    for s in snake1:
        s.cameFrom = []
    openSet = [snake1[-1]]
    closedSet = []
    dir_array1 = []
    while 1:
        current1 = min(openSet, key=lambda x: x.f)
        openSet = [openSet[i] for i in range(len(openSet)) if not openSet[i] == current1]
        closedSet.append(current1)
        for neighbor in current1.neighbors:
            if neighbor not in closedSet and not neighbor.block and neighbor not in snake1:
                temp_g = neighbor.g + 1
                if neighbor in openSet:
                    if temp_g < neighbor.g:
                        neighbor.g = temp_g
                else:
                    neighbor.g = temp_g
                    openSet.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.cameFrom = current1
        if current1 == food1:
            break
    while current1.cameFrom:
        if current1.x == current1.cameFrom.x and current1.y < current1.cameFrom.y:
            dir_array1.append(2)
        elif current1.x == current1.cameFrom.x and current1.y > current1.cameFrom.y:
            dir_array1.append(0)
        elif current1.x < current1.cameFrom.x and current1.y == current1.cameFrom.y:
            dir_array1.append(3)
        elif current1.x > current1.cameFrom.x and current1.y == current1.cameFrom.y:
            dir_array1.append(1)
        current1 = current1.cameFrom

    for i in range(rows):
        for j in range(cols):
            grid[i][j].cameFrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    return dir_array1


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.cameFrom = []
        self.block = False
        if randint(1, 600) < 8:
            self.block = True

    def show(self, color):
        draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

snake = [grid[round(rows/2)][round(cols/2)]]
food = grid[randint(0, rows-1)][randint(0, cols-1)]
current = snake[-1]
dir_array = getpath(food, snake)
food_array = [food]

flag = False

while not flag:
    clock.tick(speed)
    screen.fill((230, 230, 250))
    direction = dir_array.pop(-1)
    if direction == 0:    # down
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  # right
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2:  # up
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3:  # left
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]

    if current.x == food.x and current.y == food.y:
        while 1:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food.block or food in snake):
                break
        food_array.append(food)
        dir_array = getpath(food, snake)
    else:
        snake.pop(0)

    for spot in snake:
        spot.show((255, 0, 255))
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].block:
                grid[i][j].show((18, 18, 18))

    food.show((3, 168, 158))
    snake[-1].show((255, 69, 0))
    display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            flag = True
        elif event.type == KEYDOWN:
            if event.key == K_w and not direction == 0:
                direction = 2
            elif event.key == K_a and not direction == 1:
                direction = 3
            elif event.key == K_s and not direction == 2:
                direction = 0
            elif event.key == K_d and not direction == 3:
                direction = 1
