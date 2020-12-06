import wfdb
import random
import time

from classes.SensorTransmitter import SensorTransmitter
from classes.SensorReceiver import SensorReceiver

def featStatistics():
    ARArray = []
    FRRArray = []
    RRArray = []
    FARArray = []
    random.seed(time.time())

    for i in range(50):
        AR, FRR = testFRR(i+1, 100, 50)
        ARArray.append(AR)
        FRRArray.append(FRR)

        RR, FAR = testFAR(i+1, 100, 50)
        RRArray.append(RR)
        FARArray.append(FAR)

        print("Acceptance Rate")
        print(str(AR*100)+"%")
        print("False Rejection Rate")
        print(str(FRR*100)+"%")
        print("---------------------")
        print("Rejection Rate")
        print(str(RR*100)+"%")
        print("False Acceptance Rate")
        print(str(FAR*100)+"%")
        print("------------------------------------------")

    print("------------------------------------------")
    print("------------------------------------------")
    print("------------------------------------------")
    print("Acceptance Rate: " + str((sum(ARArray)/len(ARArray))*100) + "%")
    print(str((sum(ARArray)/len(ARArray))*100)+"%")
    print("False Rejection Rate: " + str((sum(FRRArray)/len(FRRArray))*100) + "%")
    print("---------------------")
    print("Rejection Rate: " + str((sum(RRArray)/len(RRArray))*100) + "%")
    print("False Acceptance Rate: " + str((sum(FARArray)/len(FARArray))*100) + "%")

    archive = open('analysis/featStatistics.txt', 'w')
    archive.write("\nTotal Statistics")
    archive.write("\nAcceptance Rate: " + str((sum(ARArray)/len(ARArray))*100) + "%")
    archive.write("\nFalse Rejection Rate: " + str((sum(FRRArray)/len(FRRArray))*100) + "%")
    archive.write("\n---------------------")
    archive.write("\nRejection Rate: " + str((sum(RRArray)/len(RRArray))*100) + "%")
    archive.write("\nFalse Acceptance Rate: " + str((sum(FARArray)/len(FARArray))*100) + "%")
    archive.close()

def testFRR(recordNum, iterations, sampleVariation):
    count = 0
    countFRR = 0
    print(recordNum)
    for i in range(iterations):
        sampleFrom = random.randint(0, 800)
        recordTransmitter = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=sampleFrom, channel_names=['avf'])
        #recordTransmitter = wfdb.rdrecord('samples/patient'+recordNum+'/seg01', physical=False, sampfrom=0, channel_names=['V6-Raw'])
        recordReceiver = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=sampleFrom, channel_names=['avf'])
        #recordReceiver = wfdb.rdrecord('samples/patient'+recordNum+'/seg01', physical=False, sampfrom=0, channel_names=['V6-Raw'])
        
        if(PSKAPROTOCOL(recordTransmitter, recordReceiver)):
            count = count + 1
        else:
            countFRR = countFRR + 1
    return count/iterations, countFRR/iterations

def testFAR(recordNum, iterations, sampleVariation):
    count = 0
    countFAR = 0
    recordNumT = recordNum
    for i in range(iterations):
        sampleFrom = random.randint(0, 800)

        recordNumR = random.randint(1, 200)
        while recordNumR == recordNumT:
             recordNumR = random.randint(1, 200)
        recordTransmitter = wfdb.rdrecord('samples/'+str(recordNumT), physical=False, sampfrom=sampleFrom, channel_names=['avf'])
        # recordTransmitter = wfdb.rdrecord('samples/patient'+recordNumT+'/seg01', physical=False, sampfrom=0, channel_names=['V6-Raw'])
        recordReceiver = wfdb.rdrecord('samples/'+str(recordNumR), physical=False, sampfrom=sampleFrom, channel_names=['avf'])
        # recordReceiver = wfdb.rdrecord('samples/patient'+recordNumR+'/seg01', physical=False, sampfrom=0, channel_names=['V6-Raw'])
        if(PSKAPROTOCOL(recordTransmitter, recordReceiver)):
            countFAR = countFAR + 1
        else:
            count = count + 1
    return count/iterations, countFAR/iterations

def PSKAPROTOCOL(recordTransmitter, recordReceiver):

    # Definindo frequencia e quantidade de tempo para coleta das amostras
    frequency = 500
    seconds = 10

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

featStatistics()