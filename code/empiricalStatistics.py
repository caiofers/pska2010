import wfdb
import time
import statistics
import tracemalloc

from classes.SensorTransmitter import SensorTransmitter
from classes.SensorReceiver import SensorReceiver

def timeStatistics():
    timeExtractFeatTransmitterArray = []
    timeExtractFeatReceiverArray = []
    timeGenerateLockVaultArray = []
    timeUnlockVaultArray = []
    totalTimeTransmitterArray = []
    totalTimeReceiverArray = []

    for i in range(50):
        recordTransmitter = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        recordReceiver = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        
        timeExtractFeatTransmitter, timeExtractFeatReceiver, timeGenerateLockVault, timeUnlockVault = PSKAPROTOCOLTIME(recordTransmitter, recordReceiver)

        timeExtractFeatTransmitterArray.append(timeExtractFeatTransmitter)
        timeExtractFeatReceiverArray.append(timeExtractFeatReceiver)
        timeGenerateLockVaultArray.append(timeGenerateLockVault)
        timeUnlockVaultArray.append(timeUnlockVault)
        totalTimeTransmitterArray.append(timeExtractFeatTransmitter + timeGenerateLockVault)
        totalTimeReceiverArray.append(timeExtractFeatReceiver + timeUnlockVault)

        print("\nTime to Extract Features on Transmitter: "+str(timeExtractFeatTransmitter))
        print("Time to Extract Features on Receiver: "+str(timeExtractFeatReceiver))
        print("Time to generate the locked vault on Transmitter: "+str(timeGenerateLockVault))
        print("Time to unlock vault on Receiver: "+str(timeUnlockVault))
        print("Total time: "+str(timeExtractFeatTransmitter + timeExtractFeatReceiver + timeGenerateLockVault + timeUnlockVault))

    print("\n---------------------")
    print("\nTotal statistics")

    print("\nTime to Extract Features on Transmitter")
    print("Mean: " + str(statistics.mean(timeExtractFeatTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeExtractFeatTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(timeExtractFeatTransmitterArray)))

    print("\nTime to Extract Features on Receiver")
    print("Mean: " + str(statistics.mean(timeExtractFeatReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeExtractFeatReceiverArray)))
    print("Variance: " + str(statistics.pvariance(timeExtractFeatReceiverArray)))

    print("\nTime to generate the locked vault on Transmitter")
    print("Mean: " + str(statistics.mean(timeGenerateLockVaultArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeGenerateLockVaultArray)))
    print("Variance: " + str(statistics.pvariance(timeGenerateLockVaultArray)))

    print("\nTime to unlock vault on Receiver")
    print("Mean: " + str(statistics.mean(timeUnlockVaultArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeUnlockVaultArray)))
    print("Variance: " + str(statistics.pvariance(timeUnlockVaultArray)))

    print("\nTotal Time Transmitter")
    print("Mean: " + str(statistics.mean(totalTimeTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(totalTimeTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(totalTimeTransmitterArray)))

    print("\nTotal Time Receiver")
    print("Mean: " + str(statistics.mean(totalTimeReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(totalTimeReceiverArray)))
    print("Variance: " + str(statistics.pvariance(totalTimeReceiverArray)))

    archive = open('analysis/empiricalStatistics.txt', 'w')

    archive.write("\nTotal statistics")

    archive.write("\n\nTime to Extract Features on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(timeExtractFeatTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeExtractFeatTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeExtractFeatTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nTime to Extract Features on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(timeExtractFeatReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeExtractFeatReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeExtractFeatReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nTime to generate the locked vault on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(timeGenerateLockVaultArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeGenerateLockVaultArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeGenerateLockVaultArray), 2)).replace('.', ','))

    archive.write("\n\nTime to unlock vault on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(timeUnlockVaultArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeUnlockVaultArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeUnlockVaultArray), 2)).replace('.', ','))

    archive.write("\n\nTotal Time Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(totalTimeTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(totalTimeTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(totalTimeTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nTotal Time Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(totalTimeReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(totalTimeReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(totalTimeReceiverArray), 2)).replace('.', ','))

    archive.close()

def PSKAPROTOCOLTIME(recordTransmitter, recordReceiver):

    # Definindo frequencia e quantidade de tempo para coleta das amostras
    frequency = 500
    seconds = 10

    # Definindo ordem do polinômio
    order = 8

    # Identificadores para o transmissor e receptor, respectivamente 
    IDt = 1
    IDr = 2

    # Definindo variáveis para coletar tempo
    timeExtractFeatTransmitter = 0
    timeExtractFeatReceiver = 0
    timeGenerateLockVault = 0
    timeUnlockVault = 0

    sensorTransmitter = SensorTransmitter(frequency, seconds, order, IDt, IDr)
    sensorReceiver = SensorReceiver(frequency, seconds, order, IDr)

    # Coleta dos tempos de cada etapa
    inicio = time.time()
    sensorTransmitter.extractFeats(recordTransmitter)
    fim = time.time()
    timeExtractFeatTransmitter = fim - inicio

    inicio = time.time()
    sensorReceiver.extractFeats(recordReceiver)
    fim = time.time()
    timeExtractFeatReceiver = fim - inicio

    inicio = time.time()
    vault, _ = sensorTransmitter.generateVault()
    message = sensorTransmitter.createTransmitterMessage()
    fim = time.time()
    timeGenerateLockVault = fim - inicio
    
    inicio = time.time()
    sensorReceiver.receiveTransmitterMessage(message)
    sensorReceiver.unlockVault()
    message = sensorReceiver.createAckMessage()
    fim = time.time()

    timeUnlockVault = fim - inicio
    
    sensorTransmitter.receiveAckMessage(message)
    
    return timeExtractFeatTransmitter*1000, timeExtractFeatReceiver*1000, timeGenerateLockVault*1000, timeUnlockVault*1000

timeStatistics()