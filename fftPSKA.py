from scipy import fftpack
import matplotlib.pyplot as plt
import numpy as np

def fftAply(data, nOfPoints, frequency, verbose=False, plot=False, save=False, index=None):
    if verbose: print("\nFFT - START")
    
    # Aplicando Fast Fourier Transform para 128 pontos
    X = fftpack.fft(data, n=nOfPoints)

    #Coletando a metade dos pontos da FFT, já que os pontos tem caracteristica espelhada
    X = X[0:64]

    if verbose:
        print("\nPontos da FFT:")
        print(X)
        print("\nFFT - END\n")

    if plot:
        freqs = fftpack.fftfreq(len(X)) * frequency
        __, ax = plt.subplots()

        ax.stem(freqs, np.abs(X), use_line_collection=True)
        ax.set_xlabel('Frequency in Hertz [Hz]')
        ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
        ax.set_xlim(-frequency / 2, frequency / 2)
        ax.set_ylim(-5, 125)
        
        if save: plt.savefig('graficos/fftfreqparte' + str(index) + '.png')
        plt.show()
        plt.plot(X)
        if save: plt.savefig('graficos/fftparte' + str(index) + '.png')
        plt.show()

    return X