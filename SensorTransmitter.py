from Sensor import Sensor
import ctypes
import numpy as np
import random

class SensorTransmitter(Sensor):

    def __init__(self, frequency, seconds, order, IDt, IDr):
       super().__init__(frequency, seconds, order)
       self.__IDt = IDt
       self.__IDr = IDr


    def generateVault(self):
        coeff = self.__generateCoeff() #Colocar para retornar bin e int
        
        key = []
        tamKey = 128

        bitsEachCoeff = tamKey/self._order

        for i in coeff:
            key.append(bin(ctypes.c_uint.from_buffer(ctypes.c_float(i)).value).replace('0b','')[0:int(bitsEachCoeff)])

        key = [''.join(key)] #a chave são os coeffs concatenados
        self.__commonKey = key[0].rjust(tamKey, '0')

        truePoly = []
        for feat in self._featsVector:
            truePoly.append(np.polynomial.polynomial.polyval(feat, coeff))

        chaffFeat, chaffPoly = self.__generateChaffPoints(coeff, truePoly)
        
        vault = []
        i = 0
        for i in range(len(truePoly)):
            vault.append((self._featsVector[i],truePoly[i]))

        for i in range(len(chaffPoly)):
            vault.append((chaffFeat[i],chaffPoly[i]))
        
        print("Itens no cofre: " + str(len(vault)))
        self.__lockVault(vault)
        
        return self.__vaultLocked, key    
    
    def __generateCoeff(self):
        coeff = []
        random.seed(1)
        for i in range(self._order):
            coeff.append(random.random())
        return coeff

    def __generateChaffPoints(self, coeff, truePoly):
        i = 0
        chaffFeatVector = []
        chaffPolyVector = []

        M = len(self._featsVector)/2

        while(i < M):
            chaffFeat = random.randint(0, max(self._featsVector)+100)
            if chaffFeat not in self._featsVector and chaffFeat not in chaffFeatVector:
                chaffFeatVector.append(chaffFeat)
                while(1):
                    chaffPoly = random.randint(0, int(max(truePoly)))
                    if chaffPoly != np.polynomial.polynomial.polyval(chaffFeat, coeff):
                        i = i+1
                        chaffPolyVector.append(chaffPoly)
                        break

        return chaffFeatVector, chaffPolyVector

    def __lockVault(self, vault):
        # Lock/Permutação do cofre
        random.shuffle(vault)
        self.__vaultLocked = vault


    def createTransmitterMessage(self):
        message = {}
        self.__Nounce = random.randint(0, 100)
        message["IDt"] = self.__IDt
        message["IDr"] = self.__IDr
        message["Nounce"] = self.__Nounce
        message["VAULTLOCKED"] = self.__vaultLocked
        message["MAC"] = self._macHMAC(str(self.__vaultLocked)+str(self.__Nounce)+str(self.__IDt), str(self.__commonKey))
        return message

    def receiveAckMessage(self, message):
        self.__receivedMAC = message["MAC"]
        return self.__checkMAC()

    def __checkMAC(self):
        if (self._macHMAC(str(self.__Nounce)+str(self.__IDt)+str(self.__IDr), str(self.__commonKey)) == self.__receivedMAC):
            #print("Receive with sucess")
            return True
        else:
            #print("Not received")
            return False