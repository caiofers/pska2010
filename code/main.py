
import wfdb
from classes.SensorTransmitter import SensorTransmitter
from classes.SensorReceiver import SensorReceiver

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
    order = 8

    # Identificadores para o transmissor e receptor, respectivamente 
    IDt = 1
    IDr = 2

    sensorTransmitter = SensorTransmitter(frequency, seconds, order, IDt, IDr)
    sensorReceiver = SensorReceiver(frequency, seconds, order, IDr)

    sensorTransmitter.extractFeats(recordTransmitter)
    sensorReceiver.extractFeats(recordReceiver)

    sensorTransmitter.generateVault()

    sensorReceiver.receiveTransmitterMessage(sensorTransmitter.createTransmitterMessage())
    sensorReceiver.unlockVault()
    
    return sensorTransmitter.receiveAckMessage(sensorReceiver.createAckMessage())

main()