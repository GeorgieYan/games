import pygame
import random

pygame.font.init()

game_width = 300
game_height = 600
screen_width = 800
screen_height = 700
block_size = 30

horizontal_space = (screen_width - game_width) / 2
vertical_space = screen_height - game_height

I_block = [['11011',
            '11011',
            '11011',
            '11011',
            '11111'],
           ['11111',
            '00001',
            '11111',
            '11111',
            '11111']]

O_block = [['11111',
            '11111',
            '10011',
            '10011',
            '11111']]

T_block = [['11111',
            '11011',
            '10001',
            '11111',
            '11111'],
           ['11111',
            '11011',
            '11001',
            '11011',
            '11111'],
           ['11111',
            '11111',
            '10001',
            '11011',
            '11111'],
           ['11111',
            '11011',
            '10011',
            '11011',
            '11111']]

S_block = [['11111',
            '11111',
            '11001',
            '10011',
            '11111'],
           ['11111',
            '11011',
            '11001',
            '11101',
            '11111']]

J_block = [['11111',
            '10111',
            '10001',
            '11111',
            '11111'],
           ['11111',
            '11001',
            '11011',
            '11011',
            '11111'],
           ['11111',
            '11111',
            '10001',
            '11101',
            '11111'],
           ['11111',
            '11011',
            '11011',
            '10011',
            '11111']]

Z_block = [['11111',
            '11111',
            '10011',
            '11001',
            '11111'],
           ['11111',
            '11011',
            '10011',
            '10111',
            '11111']]

L_block = [['11111',
            '11101',
            '10001',
            '11111',
            '11111'],
           ['11111',
            '11011',
            '11011',
            '11001',
            '11111'],
           ['11111',
            '11111',
            '10001',
            '10111',
            '11111'],
           ['11111',
            '10011',
            '11011',
            '11011',
            '11111']]

blocks = [I_block, O_block, T_block, S_block, J_block, Z_block, L_block]
block_colors = [(0, 255, 255), (255, 255, 0), (102, 0, 102), (0, 255, 0), (0, 0, 255), (204, 0, 0), (255, 128, 0)]

class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, column, row, block):
        self.block = block
        self.color = block_colors[blocks.index(block)]
        self.x = column
        self.y = row
        self.rotation = 0

def get_shape():
    global blocks, block_colors
    return Piece(5, 0, random.choice(blocks))

def draw_text(text, size, color, surface):
    font = pygame.font.SysFont('arial', size, bold=True)
    caption = font.render(text, 1, color)
    surface.blit(caption, (400 - caption.get_width()/2, 400))

def draw_window(surface, row, col):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 75)
    caption = font.render('Tetris', 1, (0, 102, 0))

    surface.blit(caption, (400 - caption.get_width()/2, 20))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (horizontal_space + j * 30, vertical_space + i * 30, 30, 30), 0)

    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (horizontal_space, vertical_space + i * 30), (horizontal_space + game_width, vertical_space + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (horizontal_space + j * 30, vertical_space), (horizontal_space + j * 30, vertical_space + game_height))

    pygame.draw.rect(surface, (255, 0, 0), (horizontal_space, vertical_space, game_width, game_height), 5)

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key = lambda x : x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

def convert_shape_format(block):
    positions = []
    format = block.block[block.rotation % len(block.block)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((block.x + j, block.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(block, grid):
    valid_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    valid_positions = [j for sub in valid_positions for j in sub]
    formatted = convert_shape_format(block)

    for pos in formatted:
        if pos not in valid_positions:
            if pos[1] > -1:
                return False

    return True

def check_lost(positions):
    for position in positions:
        x, y = position
        if y < 1:
            return True
    return False

def draw_next_block(block, surface):
    font = pygame.font.SysFont('arial', 30)
    caption = font.render('Next Block', 1, (255, 255, 255))
    format = block.block[block.rotation % len(block.block)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, block.color, ((horizontal_space + game_width + 50) + j * 30, (vertical_space + game_height / 2) + i * 30, 30, 30), 0)

    surface.blit(caption, (horizontal_space + game_width + 60, vertical_space + game_height / 2 - 30))

def main():
    global grid
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True

    fall_time = 0
    level_time = 0
    fall_speed = 0.15

    current_block = get_shape()
    next_block = get_shape()
    clock = pygame.time.Clock()

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 4:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_block.y += 1
            if not (valid_space(current_block, grid)) and current_block.y > 0:
                current_block.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_block.x -= 1
                    if not valid_space(current_block, grid):
                        current_block.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_block.x += 1
                    if not valid_space(current_block, grid):
                        current_block.x -= 1

                elif event.key == pygame.K_UP:
                    current_block.rotation = current_block.rotation + 1 % len(current_block.block)
                    if not valid_space(current_block, grid):
                        current_block.rotation = current_block.rotation - 1 % len(current_block.block)

                if event.key == pygame.K_DOWN:
                    current_block.y += 3
                    if not valid_space(current_block, grid):
                        current_block.y -= 3

        block_pos = convert_shape_format(current_block)

        for i in range(len(block_pos)):
            x, y = block_pos[i]
            if y > -1:
                grid[y][x] = current_block.color

        if change_piece:
            for position in block_pos:
                p = (position[0], position[1])
                locked_positions[p] = current_block.color
            current_block = next_block
            next_block = get_shape()
            change_piece = False

            if clear_rows(grid, locked_positions):
                pass

        draw_window(window, 20, 10)
        draw_next_block(next_block, window)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text("Game over! Wait till the game restarts", 40, (255, 255, 255), window)
    pygame.display.update()
    pygame.time.delay(8000)

def start_menu():
    run = True
    while run:
        window.fill((0, 0, 0))
        draw_text('Press any key to play', 75, (255, 255, 255), window)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main()
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
start_menu()
