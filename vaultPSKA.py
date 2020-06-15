import coeffPSKA
import numpy as np

def generateVault(feats, size):
    coeff = coeffPSKA.generateCoeff(feats, size) #Colocar para retornar bin e int
    print("coeff")
    print(coeff)
    key = []

    for i in coeff:
        key.append(str(i))

    key = [''.join(key)] #a chave são os coeffs concatenados

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