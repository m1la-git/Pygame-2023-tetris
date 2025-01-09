import random
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, img, scale, x, y):
        super(Button, self).__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        screen.blit(self.image, self.rect)
        return action


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos):
    grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[(x, y)]
                grid[y][x] = color
    return grid


def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(shape_format):
        for j, column in enumerate(list(line)):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(piece, grid):
    accepted_pos = [x for item in [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)] for x in
                    item]
    formatted_shape = convert_shape_format(piece)
    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True


def clear_rows(grid, locked):
    increment = 0
    index = 0
    for i in range(len(grid) - 1, -1, -1):
        grid_row = grid[i]
        if (0, 0, 0) not in grid_row:
            increment += 1
            index = i
            for j in range(len(grid_row)):
                try:
                    del locked[(j, i)]
                except ValueError:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
            x, y = key
            if y < index:
                new_key = (x, y + increment)
                locked[new_key] = locked.pop(key)
    return increment


def draw_next_shape(next_piece, screen):
    shape_format = next_piece.shape[next_piece.rotation % len(next_piece.shape)]
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(screen, next_piece.color,
                                 (top_left_x + play_width + 40 + j * block_size,
                                  top_left_y + (play_height / 2 - 100) + i * block_size, block_size, block_size), 0)
    screen.blit(pygame.font.Font('fonts/arcade.ttf', 30).render('Next shape', True, (255, 255, 255)),
                (top_left_x + play_width + 40, top_left_y + (play_height / 2) - 130))


pygame.init()

col = 10
row = 20
s_width = 600
s_height = 750
play_width = 300
play_height = 600
block_size = 30

pygame.mixer.music.load('sounds/bg.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(loops=-1)
drop_sound = pygame.mixer.Sound('sounds/drop.mp3')
drop_sound.set_volume(0.4)

bg = pygame.transform.scale(pygame.image.load('images/bg.jpeg'), (1000, s_height))
bg_x1 = 0
bg_x2 = -1000
restart_button = Button(pygame.transform.scale(pygame.image.load('images/restart.png'), (80, 80)), (1, 1), 200, 300)

top_left_x = 50
top_left_y = s_height - play_height - 50

S = [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
Z = [['.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0...', '.....']]
I = [['.....', '..0..', '..0..', '..0..', '..0..'], ['.....', '0000.', '.....', '.....', '.....']]
O = [['.....', '.....', '.00..', '.00..', '.....']]
J = [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'],
     ['.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']]
L = [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'],
     ['.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']]
T = [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'],
     ['.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.00..', '..0..', '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = ['#9e0059', '#390099', '#ff0054', '#ff5400', '#ffbd00', '#218380', '#47126b']

locked_positions = {}
create_grid(locked_positions)

change_piece = False

current_piece = Piece(5, 0, random.choice(shapes))
next_piece = Piece(5, 0, random.choice(shapes))
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.15
level_time = 0
score = 0
best_score = 0

screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
run = True
game = True
while run:
    pygame.display.update()
    clock.tick(60)
    bg_x1 += 0.4
    if bg_x1 > 1000:
        bg_x1 = bg_x1 - 1000
    bg_x2 = bg_x1 - 1000
    screen.blit(bg, (bg_x1, 0))
    screen.blit(bg, (bg_x2, 0))
    if game:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                    drop_sound.play()

                elif event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        piece_pos = convert_shape_format(current_piece)
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = Piece(5, 0, random.choice(shapes))
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

            if best_score < score:
                best_score = score

        for i in range(row):
            for j in range(col):
                if grid[i][j] != (0, 0, 0):
                    pygame.draw.rect(screen, grid[i][j],
                                     (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size))

        for i in range(row):
            pygame.draw.line(screen, '#ffe5ec', (top_left_x, top_left_y + i * block_size),
                             (top_left_x + play_width, top_left_y + i * block_size))
            for j in range(col):
                pygame.draw.line(screen, '#ffe5ec', (top_left_x + j * block_size, top_left_y),
                                 (top_left_x + j * block_size, top_left_y + play_height))

        pygame.draw.rect(screen, '#fff0f3', (top_left_x, top_left_y, play_width, play_height), 4)

        draw_next_shape(next_piece, screen)

        for pos in locked_positions:
            x, y = pos
            if y < 1:
                game = False
                break

    label = pygame.font.Font('fonts/flower.ttf', 120).render('TETRIS', True, (255, 255, 255))
    screen.blit(label, ((top_left_x + play_width / 2) - (label.get_width() / 2), 0))
    font = pygame.font.Font('fonts/arcade.ttf', 30)
    screen.blit(font.render('SCORE   ' + str(score), True, (255, 255, 255)),
                (top_left_x + play_width + 40, top_left_y + (play_height / 2) + 100))
    screen.blit(font.render('HIGHSCORE   ' + str(best_score), True, (255, 255, 255)),
                (top_left_x + play_width + 40, top_left_y + (play_height / 2) + 150))
    if not game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
        if restart_button.draw(screen):
            locked_positions = {}
            create_grid(locked_positions)
            new_game = False
            change_piece = False
            game = True
            current_piece = Piece(5, 0, random.choice(shapes))
            next_piece = Piece(5, 0, random.choice(shapes))
            clock = pygame.time.Clock()
            fall_time = 0
            fall_speed = 0.15
            level_time = 0
            score = 0

pygame.quit()
