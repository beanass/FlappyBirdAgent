import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 640))
    screen.blit(floor_surface, (floor_x_pos + 376, 640))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    # print(random_pipe_pos)
    bottom_pipe = pipe_surface.get_rect(midtop=(400, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(400, random_pipe_pos - 200))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4

    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 724:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 640:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

pygame.init()
screen_width = 376  # 576
screen_heigth = 724  # 1024

# set mode needs a tuple with a height and width of the screen
screen = pygame.display.set_mode((screen_width, screen_heigth))
clock = pygame.time.Clock()  # this will control the frame

# Game Variables
gravity = 0.17
bird_movement = 0
game_active = True

bg_surface = pygame.image.load(
    'assets/background-day.png').convert()  # read and convert in a type of image that easy to work in pygame
# bg_surface = pygame.transform.scalex(bg_surface)
bg_surface = pygame.transform.scale_by(bg_surface, 1.5)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale_by(floor_surface, 1.12)
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale_by(bird_surface, 1.5)
bird_rect = bird_surface.get_rect(center=(100, 362))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale_by(pipe_surface, 1.5)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [250, 450, 500]

while True:
    # looking for all the event that happening
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # shutdown the game completly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 362)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # screen.fill('black')
    screen.blit(bg_surface, (0, 0))  # put one surface on another surface

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -376:
        floor_x_pos = 0

    screen.blit(floor_surface, (floor_x_pos, 640))
    pygame.display.update()
    clock.tick(100)
