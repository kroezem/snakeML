import pygame
from stable_baselines3 import PPO

from train import latest
# from maze_env import MazeEnv
from snake_env import SnakeEnv

last = 0, 0


def key_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        return 0
    elif keys[pygame.K_DOWN]:
        return 1
    elif keys[pygame.K_LEFT]:
        return 2
    elif keys[pygame.K_RIGHT]:
        return 3
    return None


if __name__ == '__main__':
    env = SnakeEnv(render_mode='human')
    # env = MazeEnv('./assisted', render_mode='human')
    model = PPO.load(latest(), env)
    terminated, truncated = False, False
    obs, _ = env.reset()
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                env.close()
                exit()
            #
            elif event.type == pygame.MOUSEBUTTONDOWN:
                obs, _ = env.reset()
                model_zip = latest()
                print(f'\n******** Loading - {model_zip} ********\n')
                model = PPO.load(model_zip, env)

        action, _states = model.predict(obs)

        # action = key_input()
        # if action is None:
        #     action = last
        # last = action

        if action is not None:
            obs, rewards, terminated, truncated, info = env.step(action)
        env.render('human')

        if terminated or truncated:
            obs, _ = env.reset()

            model_zip = latest()
            print(f'\n******** Loading - {model_zip} ********\n')
            model = PPO.load(model_zip, env)
