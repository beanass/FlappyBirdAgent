import pygame
import sys
import random


class FlappyBirdGame:
    def __init__(self):
        self.screen_width = 376
        self.screen_height = 724
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.gravity = 0.17
        self.bird_movement = 0
        self.game_active = True
        self.pipe_list = []
        self.pipe_height = [250, 450, 500]

        # Load game assets
        self.load_assets()

        # Initialize game
        self.initialize_game()

    def load_assets(self):
        # Load images
        self.bg_surface = pygame.image.load('assets/background-day.png').convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface, (self.screen_width, self.screen_height))
        self.floor_surface = pygame.image.load('assets/base.png').convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface, (self.screen_width, 112))
        self.bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
        self.pipe_surface = pygame.image.load('assets/pipe-green.png').convert_alpha()

    def initialize_game(self):
        # Reset game variables
        self.bird_rect = self.bird_surface.get_rect(center=(100, self.screen_height // 2))
        self.pipe_list.clear()
        self.spawn_pipe_event = pygame.USEREVENT
        pygame.time.set_timer(self.spawn_pipe_event, 1200)

    def update_game(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= 6
                elif event.key == pygame.K_SPACE and not self.game_active:
                    self.game_active = True
                    self.initialize_game()

            elif event.type == self.spawn_pipe_event:
                self.pipe_list.extend(self.create_pipe())

        if self.game_active:
            self.bird_movement += self.gravity
            self.bird_rect.centery += self.bird_movement
            self.game_active = self.check_collision()

            # Move and draw pipes
            self.move_pipes()
            self.draw_pipes()

        # Move and draw floor
        self.move_floor()
        self.draw_floor()

        # Update the screen
        #pygame.display.update()
        #self.clock.tick(60)

        # Return the game state
        return self.get_game_state()

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(500, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 200))
        return bottom_pipe, top_pipe

    def move_pipes(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 4

        self.pipe_list = [pipe for pipe in self.pipe_list if pipe.right > 0]

    def draw_pipes(self):
        for pipe in self.pipe_list:
            if pipe.bottom >= self.screen_height:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def check_collision(self):
        if self.bird_rect.top <= 0 or self.bird_rect.bottom >= self.screen_height:
            return False

        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe):
                return False

        return True

    def move_floor(self):
        self.floor_surface_pos -= 1
        if self.floor_surface_pos <= -self.screen_width:
            self.floor_surface_pos = 0

    def draw_floor(self):
        self.screen.blit(self.floor_surface, (self.floor_surface_pos, self.screen_height - 112))
        self.screen.blit(self.floor_surface, (self.floor_surface_pos + self.screen_width, self.screen_height - 112))

    def get_game_state(self):
        bird_position = self.bird_rect.center
        pipe_positions = [pipe.centerx for pipe in self.pipe_list]
        return bird_position, pipe_positions
