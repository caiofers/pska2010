import wfdb
import time
import statistics
import tracemalloc

from SensorTransmitter import SensorTransmitter
from SensorReceiver import SensorReceiver

def timeStatistics():
    timeExtractFeatTransmitterArray = []
    timeExtractFeatReceiverArray = []
    timeGenerateLockVaultArray = []
    timeUnlockVaultArray = []
    totalTimeTransmitterArray = []
    totalTimeReceiverArray = []
    memoryPeakArray = []

    for i in range(200):
        recordTransmitter = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        recordReceiver = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        
        tracemalloc.start()
        timeExtractFeatTransmitter, timeExtractFeatReceiver, timeGenerateLockVault, timeUnlockVault = PSKAPROTOCOLTIME(recordTransmitter, recordReceiver)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        timeExtractFeatTransmitterArray.append(timeExtractFeatTransmitter)
        timeExtractFeatReceiverArray.append(timeExtractFeatReceiver)
        timeGenerateLockVaultArray.append(timeGenerateLockVault)
        timeUnlockVaultArray.append(timeUnlockVault)
        totalTimeTransmitterArray.append(timeExtractFeatTransmitter + timeGenerateLockVault)
        totalTimeReceiverArray.append(timeExtractFeatReceiver + timeUnlockVault)

        memoryPeakArray.append(peak)

        print("\nTime to Extract Features on Transmitter: "+str(timeExtractFeatTransmitter))
        print("Time to Extract Features on Receiver: "+str(timeExtractFeatReceiver))
        print("Time to generate the locked vault on Transmitter: "+str(timeGenerateLockVault))
        print("Time to unlock vault on Receiver: "+str(timeUnlockVault))
        print("Current memory usage is " + str(current) + " Bytes; Peak was " + str(peak) + " Bytes");
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

    print("\nPeak Memory Usage")
    print("Mean: " + str(statistics.mean(memoryPeakArray)) + " Bytes")
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakArray)) + " Bytes")
    print("Variance: " + str(statistics.pvariance(memoryPeakArray)) + " Bytes")
def PSKAPROTOCOLTIME(recordTransmitter, recordReceiver):

    # Definindo frequencia e quantidade de tempo para coleta das amostras
    frequency = 500
    seconds = 10

    # Definindo ordem do polinômio
    order = 5

    IDt = 1
    IDr = 2

    # Definindo variáveis para coletar tempo
    timeExtractFeatTransmitter = 0
    timeExtractFeatReceiver = 0
    timeGenerateLockVault = 0
    timeUnlockVault = 0


    sensorTransmitter = SensorTransmitter(frequency, seconds, order, IDt, IDr)
    #sensorTransmitter.setPlot(True)
    sensorReceiver = SensorReceiver(frequency, seconds, order, IDr)

    inicio = time.time()
    sensorTransmitter.extractFeats(recordTransmitter)
    fim = time.time()
    timeExtractFeatTransmitter = fim - inicio


    inicio = time.time()
    sensorReceiver.extractFeats(recordReceiver)
    fim = time.time()
    timeExtractFeatReceiver = fim - inicio
    

    inicio = time.time()
    sensorTransmitter.generateVault()
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
    
    
    return timeExtractFeatTransmitter, timeExtractFeatReceiver, timeGenerateLockVault, timeUnlockVault


timeStatistics()