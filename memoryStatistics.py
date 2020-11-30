import wfdb
import statistics
import tracemalloc

from SensorTransmitter import SensorTransmitter
from SensorReceiver import SensorReceiver

def memoryPeakStatistics():
    memoryPeakExtractFeatTransmitterArray = []
    memoryPeakExtractFeatReceiverArray = []
    memoryPeakGenerateLockVaultArray = []
    memoryPeakUnlockVaultArray = []
    totalMemoryPeakTransmitterArray = []
    totalMemoryPeakReceiverArray = []
    memoryPeakArray = []
    
    for i in range(50):
        recordTransmitter = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        recordReceiver = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        
        memoryPeakExtractFeatTransmitter, memoryPeakExtractFeatReceiver, memoryPeakGenerateLockVault, memoryPeakUnlockVault = PSKAPROTOCOLTIME(recordTransmitter, recordReceiver)

        memoryPeakExtractFeatTransmitterArray.append(memoryPeakExtractFeatTransmitter/1024)
        memoryPeakExtractFeatReceiverArray.append(memoryPeakExtractFeatReceiver/1024)
        memoryPeakGenerateLockVaultArray.append(memoryPeakGenerateLockVault/1024)
        memoryPeakUnlockVaultArray.append(memoryPeakUnlockVault/1024)
        totalMemoryPeakTransmitterArray.append(memoryPeakExtractFeatTransmitter/1024 + memoryPeakGenerateLockVault/1024)
        totalMemoryPeakReceiverArray.append(memoryPeakExtractFeatReceiver/1024 + memoryPeakUnlockVault/1024)

        print("\nMemory Peak to Extract Features on Transmitter: "+str(memoryPeakExtractFeatTransmitter/1024))
        print("Memory Peak to Extract Features on Receiver: "+str(memoryPeakExtractFeatReceiver/1024))
        print("Memory Peak to generate the locked vault on Transmitter: "+str(memoryPeakGenerateLockVault/1024))
        print("Memory Peak to unlock vault on Receiver: "+str(memoryPeakUnlockVault/1024))
        print("Total memory peak Transmitter: "+str(memoryPeakExtractFeatTransmitter/1024 + memoryPeakGenerateLockVault/1024))
        print("Total memory peak Receiver: "+str(memoryPeakExtractFeatReceiver/1024 + memoryPeakUnlockVault/1024))

    print("\n---------------------")
    print("\nTotal statistics")

    print("\nMemory Peak to Extract Features on Transmitter")
    print("Mean: " + str(statistics.mean(memoryPeakExtractFeatTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakExtractFeatTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakExtractFeatTransmitterArray)))

    print("\nMemory Peak to Extract Features on Receiver")
    print("Mean: " + str(statistics.mean(memoryPeakExtractFeatReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakExtractFeatReceiverArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakExtractFeatReceiverArray)))

    print("\nMemory Peak to generate the locked vault on Transmitter")
    print("Mean: " + str(statistics.mean(memoryPeakGenerateLockVaultArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakGenerateLockVaultArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakGenerateLockVaultArray)))

    print("\nMemory Peak to unlock vault on Receiver")
    print("Mean: " + str(statistics.mean(memoryPeakUnlockVaultArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakUnlockVaultArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakUnlockVaultArray)))

    print("\nTotal Memory Peak Transmitter")
    print("Mean: " + str(statistics.mean(totalMemoryPeakTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(totalMemoryPeakTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(totalMemoryPeakTransmitterArray)))

    print("\nTotal Memory Peak Receiver")
    print("Mean: " + str(statistics.mean(totalMemoryPeakReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(totalMemoryPeakReceiverArray)))
    print("Variance: " + str(statistics.pvariance(totalMemoryPeakReceiverArray)))


    archive = open('memoryStatistics.txt', 'w')

    archive.write("\nTotal statistics")

    archive.write("\n\nMemory Peak to Extract Features on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakExtractFeatTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakExtractFeatTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakExtractFeatTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak to Extract Features on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakExtractFeatReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakExtractFeatReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakExtractFeatReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak to generate the locked vault on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakGenerateLockVaultArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakGenerateLockVaultArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakGenerateLockVaultArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak to unlock vault on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakUnlockVaultArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakUnlockVaultArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakUnlockVaultArray), 2)).replace('.', ','))

    archive.write("\n\nTotal Memory Peak Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(totalMemoryPeakTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(totalMemoryPeakTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(totalMemoryPeakTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nTotal Memory Peak Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(totalMemoryPeakReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(totalMemoryPeakReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(totalMemoryPeakReceiverArray), 2)).replace('.', ','))

    archive.close()


def PSKAPROTOCOLTIME(recordTransmitter, recordReceiver):

    # Definindo frequencia e quantidade de tempo para coleta das amostras
    frequency = 500
    seconds = 10

    # Definindo ordem do polinômio
    order = 8

    IDt = 1
    IDr = 2

    # Definindo variáveis para coletar tempo
    memoryPeakExtractFeatTransmitter = 0
    memoryPeakExtractFeatReceiver = 0
    memoryPeakGenerateLockVault = 0
    memoryPeakUnlockVault = 0


    sensorTransmitter = SensorTransmitter(frequency, seconds, order, IDt, IDr)
    #sensorTransmitter.setPlot(True)
    sensorReceiver = SensorReceiver(frequency, seconds, order, IDr)

    tracemalloc.start()
    sensorTransmitter.extractFeats(recordTransmitter)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakExtractFeatTransmitter = peak


    tracemalloc.start()
    sensorReceiver.extractFeats(recordReceiver)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakExtractFeatReceiver = peak
    

    tracemalloc.start()
    sensorTransmitter.generateVault()
    message = sensorTransmitter.createTransmitterMessage()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakGenerateLockVault = peak

    
    
    tracemalloc.start()
    sensorReceiver.receiveTransmitterMessage(message)
    sensorReceiver.unlockVault()
    message = sensorReceiver.createAckMessage()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    memoryPeakUnlockVault = peak
    
    sensorTransmitter.receiveAckMessage(message)
    
    
    return memoryPeakExtractFeatTransmitter, memoryPeakExtractFeatReceiver, memoryPeakGenerateLockVault, memoryPeakUnlockVault


memoryPeakStatistics()