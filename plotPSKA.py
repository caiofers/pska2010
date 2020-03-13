import matplotlib.pyplot as plt
import numpy as np

def plot(xlabel, ylabel, data, filtered=True, save=False):
    plt.title(xlabel + ' X ' + ylabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if filtered == True:
        plt.plot(data)
        if save: plt.savefig('graficos/filtrado.png')

    if filtered == False:
        plt.plot(np.arange(len(data)), data)
        if save: plt.savefig('graficos/bruto.png')

    plt.show()