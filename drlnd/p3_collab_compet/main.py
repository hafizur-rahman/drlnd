import argparse
from drlnd.utils.play import Play
from drlnd.p3_collab_compet.maddpg.agent import MADDPG
from unityagents import UnityEnvironment


def parser_setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true')
    parser.add_argument('--logdir', type=str, default='output')
    parser.add_argument('--nb_episodes', type=int, default=2000)
    parser.add_argument('--nb_agents', type=int, default=2)
    parser.add_argument('--update_frequency', type=int, default=1)
    parser.add_argument('--tau', type=int, default=0.005)
    parser.add_argument('--n_step', type=int, default=1)
    parser.add_argument('--buffer_size', type=int, default=1000000)
    parser.add_argument('--batch_size', type=int, default=256)
    parser.add_argument('--warm_up_steps', type=int, default=5000)
    parser.add_argument('--gamma', type=float, default=0.99)
    parser.add_argument('--actor_lr', type=float, default=1e-4)
    parser.add_argument('--critic_lr', type=float, default=5e-4)

    args = parser.parse_args()
    dict_args = vars(args)

    return dict_args


def main(train, nb_episodes, **kwargs):
    env = UnityEnvironment(file_name="./env/Tennis.x86_64")
    agent = MADDPG(state_dim=24, action_dim=2, **kwargs)
    play = Play(env, agent, False, True)

    if train:
        play.learn(nb_episodes)
    play.eval()


if __name__ == '__main__':
    args = parser_setup()
    main(**args)
