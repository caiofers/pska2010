import random
import numpy as np

def generateCoeff(quantCoeff):
    tamBitEachInt = int(128/quantCoeff)
    maxInt = 0
    for j in range(tamBitEachInt):
        maxInt = maxInt+2**j
    coeff = []
    #maxInt = 100
    random.seed(1)
    for i in range(quantCoeff):
        coeff.append(random.randint(0, maxInt))
    return coeff

def generateChaffPoints(featVector, coeff):
    i = 0
    chaffFeatVector = []
    chaffPolyVector = []
    while(i<len(featVector)/2):
        chaffFeat = random.randint(0, max(featVector)+2*max(featVector))
        if chaffFeat not in featVector:
            chaffFeatVector.append(chaffFeat)
            while(1):
                chaffPoly = random.randint(0, max(featVector)+2*max(featVector))
                if chaffPoly != np.polynomial.polynomial.polyval(chaffFeat, coeff):
                    i = i+1
                    chaffPolyVector.append(chaffPoly)
                    break
    return chaffFeatVector, chaffPolyVector