import matplotlib.pyplot as plt
import numpy as np

import peaksPSKA
import quantizationPSKA
import fftPSKA

def calcFeats(division, frequency, verbose=False, plot=False, save=False):
    featVectorBin = []
    featVectorInt = []
    index = 0

    if verbose: print("\nCALCÚLO DAS FEATS - START")

    for data in division:
        # Aplicando Fast Fourier Transform para 128 pontos
        X = fftPSKA.fftAply(data, 128, frequency)
        
        #Encontrando os picos da FFT
        peaks = peaksPSKA.find_peaks_extended(X,10, verbose=verbose, plot=plot, save=save, index=index)

        #Aplicando a quantização para discretizar os pontos
        pt1 = quantizationPSKA.quantization(peaks, 1, verbose=verbose)
        pt2 = quantizationPSKA.quantization(X[peaks], 1, verbose=verbose)

        if plot:
            plt.plot(pt1, pt2)
            if save: plt.savefig('graficos/quantpeaks' + str(index) + '.png')
            plt.show()

        index = index + 1

        # Construindo vetor de caracteristicas com cada ponto (Cada ponto resulta em 16 bits, sendo os 8 primeiros o indices e os outros 8 o valor)
        for k in range(len(pt1)):
            featVectorBin.append(np.binary_repr(pt1[k], width=4)+np.binary_repr(pt2[k], width=4))
            featVectorInt.append(converterb_d(featVectorBin[k]))

    if verbose:
        print("Vetor de características (binário): ")
        print(featVectorBin)

        print("Vetor de características (inteiro): ")
        print(featVectorInt)
        print("\nCALCÚLO DAS FEATS - END")

    return featVectorBin, featVectorInt


def divideSamples(data, frequency, sec):
    auxData = []
    division = []
    #Dividindo as amostras em janelas (sec é a quantidade de segundos/janelas)
    for i in range(sec):
        for j in range(frequency): #(frequency é a quantidade de amostras que tem em cada segundo)
            auxData.append(data[(i + 1) * j])
        np.array(auxData)
        division.append(auxData.copy())
        auxData.clear()
    return division


def converterb_d(n):
    decimal = 0
    n = str(n)
    n = n[::-1]
    tam = len(n)
    for i in range(tam):
        if n[i] == "1":
            decimal = decimal + 2**i
    return decimal