import pygame, sys, random

import gym_flappyBird.envs.flappyBird_env


class FlappyBirdGame:

    def __init__(self):
        super().__init__()
        self.screen_width = 376  # 576
        self.screen_heigth = 724  # 1024
        # set mode needs a tuple with a height and width of the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_heigth))
        self.clock = pygame.time.Clock()  # this will control the frame

        # Game Variables
        self.gravity = 0.17
        self.bird_movement = 0
        self.game_active = True

        self.bg_surface = pygame.image.load(
            'assets/background-day.png').convert()  # read and convert in a type of image that easy to work in pygame
        # bg_surface = pygame.transform.scalex(bg_surface)
        self.bg_surface = pygame.transform.scale_by(self.bg_surface, 1.5)

        self.floor_surface = pygame.image.load('assets/base.png').convert()
        self.floor_surface = pygame.transform.scale_by(self.floor_surface, 1.12)
        self.floor_x_pos = 0

        self.bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
        self.bird_surface = pygame.transform.scale_by(self.bird_surface, 1.5)
        self.bird_rect = self.bird_surface.get_rect(center=(100, 362))

        self.pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
        self.pipe_surface = pygame.transform.scale_by(self.pipe_surface, 1.5)
        self.pipe_list = []
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)
        self.pipe_height = [250, 450, 500]

    def play(self):
        pygame.init()
        while True:
            # looking for all the event that happening
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # shutdown the game completly
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird_movement = 0
                        self.bird_movement -= 6

                    if event.key == pygame.K_SPACE and self.game_active == False:
                        self.game_active = True
                        self.pipe_list.clear()
                        self.bird_rect.center = (100, 362)
                        self.bird_movement = 0

                if event.type == self.SPAWNPIPE:
                    self.pipe_list.extend(self.create_pipe())

            # screen.fill('black')
            self.screen.blit(self.bg_surface, (0, 0))  # put one surface on another surface

            if self.game_active:
                # Bird
                self.bird_movement += self.gravity
                self.rotated_bird = self.rotate_bird(self.bird_surface)
                self.bird_rect.centery += self.bird_movement
                self.screen.blit(self.bird_surface, self.bird_rect)
                self.game_active = self.check_collision(self.pipe_list)

                # Pipes
                self.pipe_list = self.move_pipes(self.pipe_list)
                self.draw_pipes(self.pipe_list)

            # Floor
            self.floor_x_pos -= 1
            self.draw_floor()
            if self.floor_x_pos <= -376:
                self.floor_x_pos = 0

            self.screen.blit(self.floor_surface, (self.floor_x_pos, 640))
            pygame.display.update()
            self.clock.tick(100)

    def draw_floor(self):
        self.screen.blit(self.floor_surface, (self.floor_x_pos, 640))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + 376, 640))

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        # print(random_pipe_pos)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(400, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom=(400, random_pipe_pos - 200))
        return bottom_pipe, top_pipe

    def move_pipes(self, pipes):
        for pipe in pipes:
            pipe.centerx -= 4

        return pipes

    def draw_pipes(self, pipes):
        for pipe in pipes:
            if pipe.bottom >= 724:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                self.flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(self.flip_pipe, pipe)

    def check_collision(self, pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                return False
        if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 640:
            return False

        return True

    def rotate_bird(self, bird):
        new_bird = pygame.transform.rotozoom(bird, -self.bird_movement * 3, 1)
        return new_bird

    def get_game_state(self):
        # Return the current game state
        game_state = {
            'bird_position': self.bird_rect.center,  # Example: Bird position
            'pipe_positions': [pipe.center for pipe in self.pipe_list],  # Example: Pipe positions
            # Add any other relevant game state information
        }
        return game_state

    def calculate_reward(self):
        # Calculate the reward based on the current game state
        # Example implementation:
        if self.game_active:
            reward = 1.0  # Positive reward for staying alive
        else:
            reward = -1.0  # Negative reward for game over
        return reward

    def is_game_over(self):
        # Check if the game is over
        return not self.game_active

    def render(self):
        # Render the current game state
        pygame.display.update()
        self.clock.tick(100)

    def reset(self):
        # Reset the game to its initial state
        # Example implementation:
        self.bird_movement = 0
        self.game_active = True
        self.pipe_list.clear()
        self.bird_rect.center = (100, 362)
        self.floor_x_pos = 0
        # Reset any other relevant variables or game state

    def close(self):
        # Close the game and clean up any resources
        pygame.quit()
        sys.exit()

    def perform_action(self, action):
        # Perform the specified action
        if action == 0:
            # Perform movement action
            self.bird_movement = 0
            self.bird_movement -= 6
        elif action == 1:
            # Perform no movement action
            self.bird_movement += self.gravity
            # No action required, bird maintains its current movement


    def update_game(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # shutdown the game completly
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= 6

                if event.key == pygame.K_SPACE and self.game_active == False:
                    self.game_active = True
                    self.pipe_list.clear()
                    self.bird_rect.center = (100, 362)
                    self.bird_movement = 0

            if event.type == self.SPAWNPIPE:
                self.pipe_list.extend(self.create_pipe())

            # screen.fill('black')
        self.screen.blit(self.bg_surface, (0, 0))  # put one surface on another surface

        if self.game_active:
            # Bird
            #self.bird_movement += self.gravity
            self.rotated_bird = self.rotate_bird(self.bird_surface)
            self.bird_rect.centery += self.bird_movement
            self.screen.blit(self.bird_surface, self.bird_rect)
            self.game_active = self.check_collision(self.pipe_list)

            # Pipes
            self.pipe_list = self.move_pipes(self.pipe_list)
            self.draw_pipes(self.pipe_list)

        # Floor
        self.floor_x_pos -= 1
        self.draw_floor()
        if self.floor_x_pos <= -376:
            self.floor_x_pos = 0

        self.screen.blit(self.floor_surface, (self.floor_x_pos, 640))
        #pygame.display.update()
        #self.clock.tick(100)

        # Return the game state
        return self.get_game_state(), self.calculate_reward(), self.is_game_over()


def main():
    #flappyBirdGame = FlappyBirdGame()
    #flappyBirdGame.play()
    game = FlappyBirdGame()
    env = gym_flappyBird.envs.flappyBird_env.FlappyBirdEnv(game)
    observation = env.reset()
    #print(observation)

    while True:
        # Choose an action using the Gym environment
        #action = env.action_space.sample()
        print(env.action_space.sample())
        action = env.action_space.sample()
        print('action : ', action)
        # Perform the action in the environment and get the next observation, reward, done, and info
        next_observation, reward, done, info = env.step(action)
        print(next_observation)
        print(done)
        # Render the game
        env.render()

        # Update the game state using the observation
        #game.update_state(next_observation)

        # Check if the game is over
        if done:
            # Reset the environment
            observation = env.reset()

    FlappyBirdGame.close()


if __name__ == "__main__":
    main()
