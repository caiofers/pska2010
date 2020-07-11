import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import Polynomial


import filterPSKA
import featsPSKA
import coeffPSKA
import plotPSKA
import vaultPSKA
import unlockVaultPSKA



def ___main___():
    # Abrindo o arquivo com os dados ECG
    data = pd.read_csv("p000020-2183-04-28-17-471.csv", header=None)
    
    # Extraindo as linhas do arquivo, pegando a segunda coluna (II - ECG)
    data = data[1:10000][1]
    data = np.array(data).astype(int)

    #Definindo máx e min dos dados para filtar
    vMin = -15
    vMax = 15

     # Definindo frequencia e quantidade de tempo para coleta das amostras
    frequency = 125
    seconds = 5

    # Definindo ordem do polinômio
    order = 5

    vault, key = sender(data, frequency, seconds, vMin, vMax, order)
    receiver(vault, key, data, frequency, seconds, vMin, vMax, order)


def sender(data, frequency, seconds, vMin, vMax, order):

    # Pegando 625 amostras dos dados (125hz durante 5 segundos) 
    data = data[0:frequency*seconds]

    # Aplicando filtro nos dados
    data = np.array(filterPSKA.filterPSKA(data, vMin, vMax))

    # Dividindo as amostras em 5 janelas (1 janela para cada segundo) 
    division = featsPSKA.divideSamples(data, frequency, seconds)

    # Cálculo das características
    featVectorBin1, featVectorInt1 = featsPSKA.calcFeats(division, frequency)

    # Geração do cofre
    vault, key = vaultPSKA.generateVault(featVectorInt1, order)

    # Lock/Permutação do cofre
    random.shuffle(vault)

    return vault, key


def receiver(vault, key, data, frequency, seconds, vMin, vMax, order):

    # Pegando 625 amostras dos dados (125hz durante 5 segundos) 
    data = data[0:frequency*seconds]

    # Aplicando filtro nos dados
    data = np.array(filterPSKA.filterPSKA(data, vMin, vMax))

    # Dividindo as amostras em 5 janelas (1 janela para cada segundo) 
    division = featsPSKA.divideSamples(data, frequency, seconds)

    # Cálculo das características
    featVectorBin2, featVectorInt2 = featsPSKA.calcFeats(division, frequency)

    # Interseção entre as características do receiver e o cofre recebido
    intersectionArray = unlockVaultPSKA.intersection(featVectorInt2, vault)
    poly = unlockVaultPSKA.interpolateVault(intersectionArray, order)

    if (len(Polynomial(poly).coef) > order):
        print("Accepted")
    else:
        print("Not Accepted")




___main___()