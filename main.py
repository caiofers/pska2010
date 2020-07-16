import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import hashlib
from SensorTransmitter import SensorTransmitter
from SensorReceiver import SensorReceiver

def main():
    
    data = pd.read_csv("p000020-2183-04-28-17-471.csv", header=None)
    
    # Extraindo as linhas do arquivo, pegando a segunda coluna (II - ECG)
    data = data[1:10000][1]
    data = np.array(data).astype(int)

    PSKAPROTOCOL(data)
    

def PSKAPROTOCOL(data):

    # Definindo frequencia e quantidade de tempo para coleta das amostras
    frequency = 125
    seconds = 5

    # Definindo ordem do polinômio
    order = 5

    filterMin = -15
    filterMax = 15

    IDt = 1
    IDr = 2

    sensorTransmitter = SensorTransmitter(frequency, seconds, order, filterMin, filterMax, IDt, IDr)
    sensorReceiver = SensorReceiver(frequency, seconds, order, filterMin, filterMax, IDr)

    sensorTransmitter.extractFeats(data)
    sensorReceiver.extractFeats(data)

    sensorTransmitter.generateVault()

    sensorReceiver.receiveTransmitterMessage(sensorTransmitter.createTransmitterMessage())
    sensorReceiver.unlockVault()
    
    sensorTransmitter.receiveAckMessage(sensorReceiver.createAckMessage())

main()