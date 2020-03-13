from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np

def find_peaks_extended(data, height, verbose=False, plot=False, save=False, index=None):

    if verbose: print("\nDETECÇÃO DE PICOS - START")

    peaks, _ = find_peaks(data, height=height)

    if verbose:
        print("\nDados:")
        print(data)
        print("\nIndices dos picos encontrados:")
        print(peaks)
        print("\nValores dos picos encontrados:")
        print(data[peaks])
        print("\nDETECÇÃO DE PICOS - END\n")
    
    if plot:
        plt.plot(data)
        plt.plot(peaks, data[peaks], "x")
        plt.plot(np.zeros_like(data), "--", color="gray")
        if save: plt.savefig('graficos/peaksparte' + str(index) + '.png')
        plt.show()
    return peaks