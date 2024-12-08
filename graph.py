import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import LinearLocator

from black_jack import BlackJack
from monte_carlo import MonteCarlo
from sarsa import SARSA
from q_learning import QLearning


def plot_algorithm(algorithm_class):
    algorithm = algorithm_class()
    algorithm.train(10000)

    ax = plt.figure().add_subplot(projection='3d')

    # Make data.
    X = np.arange(12, 21+1, 1, dtype=np.int32)
    xlen = len(X)
    Y = np.arange(2, 11+1, 1, dtype=np.int32)
    ylen = len(Y)

    Z = []
    for j in Y:
        new_list = []
        for i in X:
            state = BlackJack.make_state(player_sum=i, player_has_ace=0, dealer_sum=j)
            new_list.append(algorithm.get_state_value(state))
        Z.append(new_list)
    Z = np.array(Z, dtype=np.float32)
    X, Y = np.meshgrid(X, Y)

    colortuple = ('y', 'b')
    colors = np.empty(X.shape, dtype=str)
    for y in range(ylen):
        for x in range(xlen):
            colors[y, x] = colortuple[(x + y) % len(colortuple)]

    # Plot the surface with face colors taken from the array we made.
    surf = ax.plot_surface(X, Y, Z, facecolors=colors, linewidth=0)

    # Customize the z axis.
    ax.set_zlim(-1, 1)
    ax.zaxis.set_major_locator(LinearLocator(6))

    plt.show()





if __name__ == "__main__":
    plot_algorithm(QLearning)

