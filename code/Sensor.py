import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal
import pandas as pd
import hashlib
import random
import hmac
import base64
import binascii

class Sensor:

    # Inicialização do sensor com número de bloco e ID
    def __init__(self, frequency, seconds, order):
        self.__frequency = frequency
        self.__seconds = seconds
        self._order = order
        self.__verbose = False
        self.__plot = False
        self.__savePlot = False
    
    def setVerbose(self, verbose=False):
        self.__verbose = verbose
    
    def setPlot(self, plot=False, savePlot=False):
        self.__plot = plot
        self.__savePlot = savePlot

    def extractFeats(self, record):

        data =[]

        for i in range(len(record.d_signal)):
            data.extend(record.d_signal[i])

        # Pegando amostras dos dados 
        data = data[0:int(self.__frequency*self.__seconds)]

        # Dividindo as amostras em janelas 
        division = self.__divideSamples(data)

        # Cálculo das características
        self._featsVector = self.__calcFeats(division)
        return self._featsVector

    def __plotPy(self, xlabel, ylabel, data):
        plt.title(xlabel + ' X ' + ylabel)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.plot(data)
        if self.__savePlot: plt.savefig('graficos/'+ylabel)
        plt.show()

    def __divideSamples(self, data):
        auxData = []
        division = []

        #Definindo numero de janelas
        numOfWindows = 8

        #Dividindo as amostras em janelas de controlada 
        for i in range(numOfWindows):
            for j in range(int(len(data)/numOfWindows)):
                auxData.append(data[(i + 1) * j])
            np.array(auxData)
            division.append(auxData.copy())
            auxData.clear()
        return division

    def __calcFeats(self, division):
        featVectorBin = []
        featVectorInt = []

        index = 0

        if self.__verbose: print("\nCALCÚLO DAS FEATS - INÍCIO")

        for data in division:
            # Aplicando Fast Fourier Transform para 128 pontos
            X = self.__fftAply(data, 128, index)

            # Definindo tamanho mínimo dos picos a serem detectados
            vMaxHeight = 5

            #Encontrando os picos da FFT
            peaks = self.__findPeaks(X, vMaxHeight, index)
            if len(peaks) == 0:
                return featVectorInt

            # Definindo numero de bits da quantização
            nQuantBitsValue = 4
            nQuantBitsIndex = 4

            #Aplicando a quantização para discretizar os pontos
            pt1 = self.__quantization(peaks, nQuantBitsIndex)
            pt2 = self.__quantization(X[peaks], nQuantBitsValue)

            if self.__plot:
                plt.title("Dados quantizados")
                plt.plot(pt1, pt2)
                if self.__savePlot: plt.savefig('graficos/quantpeaks' + str(index) + '.png')
                plt.show()
                index = index + 1

           # Construindo vetor de características com cada ponto (Cada ponto resulta em 16 bits, sendo os 8 primeiros o indices e os outros 8 o valor)
            for k in range(len(pt1)):
                featVectorBin.append(np.binary_repr(pt1[k], width=4)+np.binary_repr(pt2[k], width=4))
                featVectorInt.append(self.__convertBinToInt(featVectorBin[k]))


        if self.__verbose:
            print("Vetor de características (binário): ")
            print(featVectorBin)
            print("\nCALCÚLO DAS FEATS - FIM")

        return featVectorInt

        
    
    def __fftAply(self, data, nOfPoints, index=None):
        if self.__verbose: print("\nFFT - INÍCIO")
        
        # Aplicando Fast Fourier Transform para 128 pontos
        X = fftpack.fft(data, n=nOfPoints)

        # Coletando a metade dos pontos da FFT, já que os pontos tem característica espelhada
        X = X[0:64]

        if self.__verbose:
            print("\nPontos da FFT:")
            print(X)
            print("\nFFT - FIM\n")

        if self.__plot:
            freqs = fftpack.fftfreq(len(X)) * self.__frequency
            __, ax = plt.subplots()

            ax.stem(freqs, np.abs(X), use_line_collection=True)
            ax.set_xlabel('Frequency in Hertz [Hz]')
            ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
            ax.set_xlim(-self.__frequency / 2, self.__frequency / 2)
            #ax.set_ylim(-5, self.__frequency)
            
            if self.__savePlot: plt.savefig('graficos/fftfreqparte' + str(index) + '.png')
            plt.title("FFT Freq")
            plt.show()

            plt.title("FFT")
            plt.plot(X)
            if self.__savePlot: plt.savefig('graficos/fftparte' + str(index) + '.png')
            plt.show()

        return X

    # Encontrar os picos da FFT
    def __findPeaks(self, data, height, index=None):
        if self.__verbose: print("\nDETECÇÃO DE PICOS - START")
        peaks, _ = signal.find_peaks(data)

        if self.__verbose:
            print("\nDados:")
            print(data)
            print("\nIndices dos picos encontrados:")
            print(peaks)
            print("\nValores dos picos encontrados:")
            print(data[peaks])
            print("\nDETECÇÃO DE PICOS - END\n")
        
        if self.__plot:
            plt.title("Picos")
            plt.plot(data)
            plt.plot(peaks, data[peaks], "x")
            plt.plot(np.zeros_like(data), "--", color="gray")
            if self.__savePlot: plt.savefig('graficos/peaksparte' + str(index) + '.png')
            plt.show()
        return peaks

    def __quantization(self, data, nQuantBits):
        if self.__verbose: print("\nQUANTIZAÇÃO - INÍCIO")

        # Criação de uma lista vazia para armazenar os coeficientes quantizados
        quantized_coeffs = []

        if len(data) != 0:
            # Definindo limite superior e inferior dos dados a serem quantizados
            vMax = max(data)
            vMin = min(data)

            # Definindo o número de níveis de acordo com a quantidade de bits
            nLevels = 2^nQuantBits

            # Definindo distância entre os níveis
            distLevels = (vMax-vMin)/nLevels

            # Quantização de cada um dos valores da lista de dados 
            for d in data:
                level = 0
                limiar = vMin+(level+1)*distLevels
                while(d > limiar and limiar < vMax):
                    level = level + 1
                    limiar = vMin+(level+1)*distLevels
                quantized_coeffs.append(level)

            if self.__verbose:
                print("\nDados:")
                print(data)
                print("\nDados Quantizados:")
                print(quantized_coeffs)
                print("\nQUANTIZAÇÃO - FIM\n")
        
        return quantized_coeffs
    
    # Converter binário para inteiro
    def __convertBinToInt(self, n):
        decimal = 0
        n = str(n)
        n = n[::-1]
        tam = len(n)
        for i in range(tam):
            if n[i] == "1":
                decimal = decimal + 2**i
        return decimal
    
    def _macHMAC(self, message, key):
        key = bytes(key, 'UTF-8')
        message = bytes(message, 'UTF-8')
        digester = hmac.new(key, message, hashlib.sha1)
        signature1 = digester.digest()
        signature2 = base64.urlsafe_b64encode(signature1)
        
        return str(signature2, 'UTF-8')