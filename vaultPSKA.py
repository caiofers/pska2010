import coeffPSKA
import numpy as np
import ctypes

def generateVault(feats, size):
    coeff = coeffPSKA.generateCoeff(feats, size) #Colocar para retornar bin e int
    print("coeff")
    print(coeff)
    key = []
    tamKey = 128

    bitsEachCoeff = tamKey/size

    for i in coeff:
        key.append(bin(ctypes.c_uint.from_buffer(ctypes.c_float(i)).value).replace('0b','')[0:int(bitsEachCoeff)])

    key = [''.join(key)] #a chave são os coeffs concatenados
    key = key[0].rjust(tamKey, '0')

    truePoly = []
    for feat in feats:
        truePoly.append(np.polynomial.polynomial.polyval(feat, coeff))

    chaffFeat, chaffPoly = coeffPSKA.generateChaffPoints(feats, coeff, truePoly)
    
    vault = []
    i = 0
    for i in range(len(truePoly)):
        vault.append((feats[i],truePoly[i]))

    for i in range(len(chaffPoly)):
        vault.append((chaffFeat[i],chaffPoly[i]))
    
    return vault, key