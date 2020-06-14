import random
import numpy as np

def generateCoeff(featVector, quantCoeff):
    coeff = []
    random.seed(1)
    for i in range(quantCoeff):
        coeff.append(random.random())
    return coeff

def generateChaffPoints(featVector, coeff, truePoly):
    i = 0
    chaffFeatVector = []
    chaffPolyVector = []

    maxChaffPoly = np.mean(truePoly)
    while(i<len(featVector)/2):
        chaffFeat = random.randint(0, max(featVector))
        if chaffFeat not in featVector and chaffFeat not in chaffFeatVector:
            chaffFeatVector.append(chaffFeat)
            while(1):
                chaffPoly = random.randint(0, int(max(truePoly)))
                if chaffPoly != np.polynomial.polynomial.polyval(chaffFeat, coeff):
                    i = i+1
                    chaffPolyVector.append(chaffPoly)
                    break
    return chaffFeatVector, chaffPolyVector