from pygame import display, time, draw, font as pgfont, QUIT, init
from random import randint
import pygame
from numpy import sqrt

init()

# Initializing game parameters

speed = 12  # Game speed

width = 600  # Board width
board_height = 600  # Board height
panel_height = 44  # Score panel height
height = board_height + panel_height  # Window height
cols = 50  # Columns in the board
rows = 50  # Rows in the board
wr = width / cols  # Cell width
hr = board_height / rows  # Cell height

# Colour palette
BG_COLOR = (18, 19, 28)
GRID_COLOR = (30, 31, 46)
BLOCK_COLOR = (72, 74, 94)
BLOCK_HIGHLIGHT = (96, 98, 122)
SNAKE_BODY_COLOR = (0, 200, 132)
SNAKE_BODY_SHADE = (0, 150, 100)
SNAKE_HEAD_COLOR = (255, 209, 102)
FOOD_COLOR = (255, 71, 87)
FOOD_GLOW = (120, 30, 40)
PANEL_COLOR = (12, 13, 20)
TEXT_COLOR = (230, 230, 240)
ACCENT_COLOR = (0, 200, 132)

screen = display.set_mode([width, height])
display.set_caption("HUNGRY NIGEL - Self-Playing Snake")
clock = time.Clock()
score_font = pgfont.SysFont("Consolas", 22, bold=True)
title_font = pgfont.SysFont("Consolas", 22, bold=True)


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

    def show(self, color, radius=4):
        draw.rect(screen, color, [self.x * hr + 2, self.y * wr + 2, hr - 4, wr - 4], border_radius=radius)

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


def draw_grid():
    for i in range(cols + 1):
        x = i * wr
        draw.line(screen, GRID_COLOR, (x, 0), (x, board_height))
    for j in range(rows + 1):
        y = j * hr
        draw.line(screen, GRID_COLOR, (0, y), (width, y))


def draw_panel(length):
    draw.rect(screen, PANEL_COLOR, [0, board_height, width, panel_height])
    draw.line(screen, ACCENT_COLOR, (0, board_height), (width, board_height), 2)
    title_surface = title_font.render("HUNGRY NIGEL", True, ACCENT_COLOR)
    screen.blit(title_surface, (16, board_height + (panel_height - title_surface.get_height()) // 2))
    score_surface = score_font.render(f"Length: {length}", True, TEXT_COLOR)
    screen.blit(score_surface, (width - score_surface.get_width() - 16,
                                 board_height + (panel_height - score_surface.get_height()) // 2))


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
    screen.fill(BG_COLOR)
    draw_grid()

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

    for i in range(rows):
        for j in range(cols):
            if grid[i][j].block:
                grid[i][j].show(BLOCK_COLOR, radius=2)

    for spot in snake[:-1]:
        spot.show(SNAKE_BODY_COLOR, radius=6)
    snake[-1].show(SNAKE_HEAD_COLOR, radius=8)

    food.show(FOOD_COLOR, radius=10)

    draw_panel(len(snake))

    display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            flag = True
