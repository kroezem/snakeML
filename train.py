import glob
import os
from datetime import datetime

from stable_baselines3 import PPO
from snake_env import SnakeEnv

NAME = '5x5_2'


def latest():
    model_files = glob.glob(os.path.join(f'./models/{NAME}', "*.zip"))
    if not model_files:
        return None
    latest_model = max(model_files, key=os.path.getctime)
    return latest_model


if __name__ == "__main__":
    # env = MazeEnv('./assisted')
    env = SnakeEnv(rows=16, cols=16)

    model_zip = latest()
    if model_zip:
        print(f'\n******** Loading - {model_zip} ********\n')
        model = PPO.load(model_zip, env)
    else:
        print(f'\n******** Creating - {NAME} ********\n')
        model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=f"./logs/{NAME}")

    while True:
        model.learn(total_timesteps=20_000, reset_num_timesteps=False)
        print(f'\n******** SAVING - {NAME} ********\n')
        model.save(f'./models/{NAME}/{datetime.now().strftime("%Y%m%d_%H%M%S")}')
