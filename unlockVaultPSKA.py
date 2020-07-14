import coeffPSKA
import numpy as np
from scipy.interpolate import lagrange
import ctypes


def unlock():
    print()


def intersection(feats, vault):
    intersectionArray = []

    for i in vault:
        if(i[0] in feats):
            #if(i not in intersectionArray):
                intersectionArray.append(i)
    return intersectionArray

def interpolateVault(intersectionArray, order):
    b = []
    c = []
    for i in intersectionArray:
        if(i[0] not in b):
            b.append(i[0])
            c.append(i[1])
    poly = lagrange(b, c)
    key = []
    tamKey = 128
    bitsEachCoeff = tamKey/order
    for i in range(order):
        key.append(bin(ctypes.c_uint.from_buffer(ctypes.c_float(poly[i])).value).replace('0b','')[0:int(bitsEachCoeff)])

    key = [''.join(key)] #a chave são os coeffs concatenados
    key = key[0].rjust(tamKey, '0')

    return key
    

