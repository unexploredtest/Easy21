import random

from common import bournoli
from black_jack import BlackJack

class QLearning:
    def __init__(self):
        self.Ns = None
        self.Qs = None
        self.env = None
        self.N0 = 100
        self.state_size = 2**11
        self.epsilon = None
        self.reset()

    def train(self, episodes):
        for i in range(episodes):
            end_result = None

            action = self.get_action()
            current_state = self.env.get_state()
            current_state_action = BlackJack.get_bin_rep(current_state, action)
            while(True):
                end_result = self.env.step(action)
                if(self.env.is_finished):
                    break

                self.Ns[current_state_action] += 1

                next_action = self.get_action()
                next_state = self.env.get_state()
                next_state_action = BlackJack.get_bin_rep(next_state, next_action)

                self.Qs[current_state_action] = self.Qs[current_state_action] + (1 / self.Ns[current_state_action])*(self.get_state_value(next_state) - self.Qs[current_state_action])

                action = next_action
                current_state = next_state
                current_state_action = next_state_action

            values = {"win": 1, "draw": 0, "def": -1}
            end_value = values[end_result]
            self.Ns[current_state_action] += 1
            

            self.Qs[current_state_action] = self.Qs[current_state_action] + (1 / self.Ns[current_state_action])*(end_value - self.Qs[current_state_action])

            self.env.reset()

    def get_action(self):
        action = None

        take_state = BlackJack.get_bin_rep(self.env.get_state(), "take")
        stick_state = BlackJack.get_bin_rep(self.env.get_state(), "stick")
        

        total_N = self.Ns[take_state] + self.Ns[stick_state]
        self.epsilon = self.N0 / (self.N0+total_N)
        if(bournoli(self.epsilon)):
            action = random.choice(["take", "stick"])
        else:
            take_value = self.Qs[take_state]
            stick_value = self.Qs[stick_state]

            # Hmmm
            if(take_value < stick_value):
                action = "stick"
            else:
                action = "take"

        return action

    def get_action_value(self, state, action):
        desired_state = BlackJack.get_bin_rep(state, action)
        return self.Qs[desired_state]

    def get_state_value(self, state):
        take_action = BlackJack.get_bin_rep(state, "take")
        take_value = self.Qs[take_action]

        stick_action = BlackJack.get_bin_rep(state, "stick")
        stick_value = self.Qs[stick_action]

        return max(take_value, stick_value)

    def reset(self):
        self.Ns = [0]*(self.state_size)
        self.Qs = [0]*(self.state_size)
        self.epsilon = 1
        self.env = BlackJack()


if __name__ == "__main__":
    lol = SARSA()
    lol.train(10000)
    d_state = BlackJack.make_state(player_sum=21, player_has_ace=0, dealer_sum=8)
    print("Take:", lol.get_action_value(d_state, "take"))
    print("Stick:", lol.get_action_value(d_state, "stick"))
    print("Value:", lol.get_state_value(d_state))