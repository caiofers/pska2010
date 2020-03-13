import coeffPSKA
import numpy as np

def generateVault(feats, size):
    coeff = coeffPSKA.generateCoeff(size) #Colocar para retornar bin e int
    key = coeff #coeff é a chave
    truePoly = np.polynomial.polynomial.polyval(feats, coeff)
    print(feats, truePoly)
    chaffFeat, chaffPoly = coeffPSKA.generateChaffPoints(feats, coeff)

    vault = []
    i = 0
    for i in range(len(truePoly)):
        vault.append((feats[i],truePoly[i]))

    for i in range(len(chaffPoly)):
        vault.append((chaffFeat[i],chaffPoly[i]))
    
    return vault, key