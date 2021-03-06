import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def _hidden_init(input):
    size = input.data.size()[0]
    val = 1 / np.sqrt(size)
    return -val, val


class Actor(nn.Module):
    def __init__(self, action_dim, state_dim):
        super(Actor, self).__init__()

        self._state_dim = state_dim

        self._a_fc_1 = nn.Linear(state_dim, 128)
        self._action = nn.Linear(128, action_dim)

        self.initialize_parameters()

    def initialize_parameters(self):
        self._a_fc_1.weight.data.uniform_(*_hidden_init(self._a_fc_1.weight))
        self._a_fc_1.bias.data.uniform_(*_hidden_init(self._a_fc_1.bias))
        self._action.weight.data.uniform_(-3e-3, 3e-3)
        self._action.bias.data.uniform_(-3e-3, 3e-3)

    def forward(self, state):
        x = F.relu(self._a_fc_1(state))
        x = torch.tanh(self._action(x))

        return x


class Critic(nn.Module):
    def __init__(self, action_dim, state_dim):
        super(Critic, self).__init__()

        self._state_dim = state_dim
        self._action_dim = action_dim
        self._c_fc_1 = nn.Linear(state_dim, 128)
        self._c_fc_2 = nn.Linear(128 + action_dim, 128)
        self._q_value = nn.Linear(128, 1)

        self.initialize_parameters()

    def initialize_parameters(self):
        self._c_fc_1.weight.data.uniform_(*_hidden_init(self._c_fc_1.weight))
        self._c_fc_1.bias.data.uniform_(*_hidden_init(self._c_fc_1.bias))
        self._c_fc_2.weight.data.uniform_(*_hidden_init(self._c_fc_2.weight))
        self._c_fc_2.bias.data.uniform_(*_hidden_init(self._c_fc_2.bias))
        self._q_value.weight.data.uniform_(-3e-4, 3e-4)
        self._q_value.bias.data.uniform_(-3e-4, 3e-4)

    def forward(self, state, action):

        x = F.relu(self._c_fc_1(state))
        x = torch.cat((x, action), dim=1)
        x = F.relu(self._c_fc_2(x))
        x = self._q_value(x)

        return x
