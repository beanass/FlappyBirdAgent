import pygame
from gym_flappyBird.envs.flappyBird_env import FlappyBirdEnv

pygame.init() # initialize pygame
clock = pygame.time.Clock()
window = pygame.display.set_mode((1000, 500))
env = FlappyBirdEnv()
run = True
while run:
    clock.tick(30) # set game speed to 30 fps
    action = [] #, get action
    env.step(action) # calculate game step
    env.render() # make pygame render calls to window
    pygame.display.update() # update window
pygame.quit()


