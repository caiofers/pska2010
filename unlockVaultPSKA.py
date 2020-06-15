import coeffPSKA
import numpy as np
from scipy.interpolate import lagrange



def unlock():
    print()


def intersection(feats, vault):
    print("feats")
    
    intersectionArray = []

    for i in vault:
        if(i[0] in feats):
            #if(i not in intersectionArray):
                intersectionArray.append(i)
    return intersectionArray

def interpolateVault(intersectionArray, order):
    b = []
    c = []
    count = 0
    for i in intersectionArray:
        if(i[0] not in b):
            b.append(i[0])
            c.append(i[1])
    print(b)
    print(c)
    poly = lagrange(b, c)
    return poly
    

