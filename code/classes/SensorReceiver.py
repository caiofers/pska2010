from Sensor import Sensor
import ctypes
from scipy.interpolate import lagrange

import random

class SensorReceiver(Sensor):

    def __init__(self, frequency, seconds, order, IDr):
       super().__init__(frequency, seconds, order)
       self.__IDr = IDr

    # Desmembrando a mensagem recebido do transmissor
    def receiveTransmitterMessage(self, message):
        self.__IDt = message["IDt"] 
        self.__Nounce = message["Nounce"]
        self.__lockedVault = message["VAULTLOCKED"]
        self.__receivedMAC = message["MAC"]

    # Destrancar o cofre encontrando os pontos de interseção
    def unlockVault(self):
        intersection = self.__intersection()
        self.__interpolateVault(intersection)
        self.__checkMAC()

    def __intersection(self):
        intersectionArray = []

        for i in self.__lockedVault:
            if(i[0] in self._featsVector):
                intersectionArray.append(i)
        return intersectionArray

    # Interpolação dos pontos para encontrar o polinômio
    def __interpolateVault(self, intersectionArray):
        
        # Listas para extrair o valor de varíavel e o resultado que aquela variável gera
        b = []
        c = []
        for i in intersectionArray:
            if(i[0] not in b):
                b.append(i[0])
                c.append(i[1])
        
        # Interpolação dos pontos
        poly = lagrange(b, c)
        key = []
        tamKey = 128
        bitsEachCoeff = tamKey/self._order
        for i in range(self._order):
            key.append(bin(ctypes.c_uint.from_buffer(ctypes.c_float(poly[i])).value).replace('0b','')[0:int(bitsEachCoeff)])

        key = [''.join(key)] # A chave são os coeffs concatenados
        self.__keyCommon = key[0].rjust(tamKey, '0') # Completando o tamanho da chave

        return key

    def __checkMAC(self):
        if (self._macHMAC(str(self.__lockedVault)+str(self.__Nounce)+str(self.__IDt), str(self.__keyCommon)) == self.__receivedMAC):
            #print("Accepted")
            return True
        else:
            #print("Not Accepted")
            return False

    def createAckMessage(self):
        message = {}
        message["MAC"] = self._macHMAC(str(self.__Nounce)+str(self.__IDt)+str(self.__IDr), str(self.__keyCommon))
        return message
    
    