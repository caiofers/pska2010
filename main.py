
import wfdb
import pandas as pd
import hashlib
from SensorTransmitter import SensorTransmitter
from SensorReceiver import SensorReceiver



def main():
    recordNum = 1
    recordTransmitter = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=0, channel_names=['avf'])
    recordReceiver = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=0, channel_names=['avf'])
    PSKAPROTOCOL(recordTransmitter, recordReceiver)



def PSKAPROTOCOL(recordTransmitter, recordReceiver):

    # Definindo frequencia e quantidade de tempo para coleta das amostras
    frequency = 500
    seconds = 2

    # Definindo ordem do polinômio
    order = 5

    IDt = 1
    IDr = 2

    sensorTransmitter = SensorTransmitter(frequency, seconds, order, IDt, IDr)
    #sensorTransmitter.setPlot(True)
    sensorReceiver = SensorReceiver(frequency, seconds, order, IDr)

    sensorTransmitter.extractFeats(recordTransmitter)
    sensorReceiver.extractFeats(recordReceiver)

    sensorTransmitter.generateVault()

    sensorReceiver.receiveTransmitterMessage(sensorTransmitter.createTransmitterMessage())
    sensorReceiver.unlockVault()
    
    return sensorTransmitter.receiveAckMessage(sensorReceiver.createAckMessage())





main()