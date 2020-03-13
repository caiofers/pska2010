import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import filterPSKA
import featsPSKA
import coeffPSKA
import plotPSKA
import vaultPSKA



def ___main___():
    # Abrindo o arquivo com os dados ECG
    data = pd.read_csv("p000020-2183-04-28-17-47.csv", header=None)
    
    # Extraindo as linhas do arquivo, pegando a segunda coluna (II - ECG)
    x = data[1:10000][1]
    x = np.array(x).astype(int)

    data = filterPSKA.filterPSKA(x, 10, -10)

    data1 = np.array(data[100:725])
    data2 = np.array(data[105:730])

    division = featsPSKA.divideSamples(data1, 125, 5)
    featVectorBin1, featVectorInt1 = featsPSKA.calcFeats(division, 125)

    #print(concat1)
    #plt.plot(concat1)
    #plt.savefig('graficos/concatenado1.png')
    #plt.show()

    #featVector2 = divideSamples(data2, 125, 5)
    #plt.plot(concat1)
    #plt.savefig('graficos/concatenado2.png')
    #plt.show()

    tamPoly = 10
    coeff = coeffPSKA.generateCoeff(tamPoly+1) #Colocar para retornar bin e int
    key = coeff #coeff é a chave
    truePoly = np.polynomial.polynomial.polyval(featVectorInt1, coeff)
    print(featVectorInt1, truePoly)
    chaffFeat, chaffPoly = coeffPSKA.generateChaffPoints(featVectorInt1, coeff)

    vault = []
    i = 0
    for i in range(len(truePoly)):
        vault.append((featVectorInt1[i],truePoly[i]))

    for i in range(len(chaffPoly)):
        vault.append((chaffFeat[i],chaffPoly[i]))

    #vault = vaultPSKA.generateVault(featVectorInt1, 11)

    print("TESTE VAULT\n\n")
    print(vault)
    random.shuffle(vault)
    print(vault)

    '''
    quant1 = quantization(concat1, 4)
    plt.plot(quant1)
    plt.savefig('graficos/quantizado.png')
    plt.show()
    quant2 = quantization(concat2, 4)
    plt.plot(quant1)
    plt.plot(quant2)
    plt.savefig('graficos/cruzamento.png')
    plt.show()


    freqs = fftpack.fftfreq(len(quant1)) * 125
    fig, ax = plt.subplots()
    ax.stem(freqs, np.abs(quant1), use_line_collection=True)
    ax.set_xlabel('Frequency in Hertz [Hz]')
    ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
    ax.set_xlim(-125 / 2, 125 / 2)
    ax.set_ylim(-5, 20)
    plt.show()
    freqs = fftpack.fftfreq(len(quant2)) * 125
    fig, ax = plt.subplots()
    ax.stem(freqs, np.abs(quant2), use_line_collection=True)
    ax.set_xlabel('Frequency in Hertz [Hz]')
    ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
    ax.set_xlim(-125 / 2, 125 / 2)
    ax.set_ylim(-5, 20)
    plt.show()
    #plotPSKA.plot('Sample', 'II w/ Filter', data)
    #plotPSKA.plot('Sample', 'II w/ Filter Ordered', sample, sorted(data))

    plotPSKA.plot('Sample', 'AVF', sampleAVF, AVF)
    sample, data = filterPSKA.filterPSKA(sampleAVF, AVF, 50, -50)
    plotPSKA.plot('Sample', 'AVF w/ Filter', sample, data)
    #plotPSKA.plot('Sample', 'AVF w/ Filter Ordered', sample, sorted(data))

    plotPSKA.plot('Sample', 'ABP', sampleABP, ABP)
    sample, data = filterPSKA.filterPSKA(sampleABP, ABP, 150, 50)
    plotPSKA.plot('Sample', 'ABP w/ Filter', sample, data)
    #plotPSKA.plot('Sample', 'ABP w/ Filter Ordered', sample, sorted(data))

    plotPSKA.plot('Sample', 'PAP', samplePAP, PAP)
    sample, data = filterPSKA.filterPSKA(samplePAP, PAP, 150, 30)
    plotPSKA.plot('Sample', 'PAP w/ Filter', sample, data)
    #plotPSKA.plot('Sample', 'PAP w/ Filter Ordered', sample, sorted(data))
    '''


___main___()