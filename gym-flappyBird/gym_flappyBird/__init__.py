from gym.envs.registration import register

register(
    id='flappybird-v0',
    entry_point='gym_flappyBird.envs:FlappyBirdEnv',
)
register(
    id='foo-extrahard-v0',
    entry_point='gym_flappyBird.envs:FooExtraHardEnv',
)