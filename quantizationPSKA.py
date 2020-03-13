import numpy as np

def quantization(data, bits, verbose=False):
    
    if verbose == True: print("\nQUANTIZAÇÃO - START")
    
    quantized_coeffs = []

    for key in data:
        sig = key * (2 ** bits - 1)
        sig = np.round(sig)
        sig = np.array(sig).astype(int)
        # print(sig)
        quantized_coeffs.append(sig)
    
    quantized_coeffs = np.array(quantized_coeffs)

    if verbose == True:
        print("\nDados:")
        print(data)
        print("\nDados Quantizados:")
        print(quantized_coeffs)
        print("\nQUANTIZAÇÃO - END\n")
    
    return quantized_coeffs

'''
def quantization(data, qBlocks, bits):
    f_s = 125
    qtDados = len(data)
    #print(data)
    qCoef = qtDados/qBlocks
    quantized_coeffs = []

    for key in data:
        sig = key * (2 ** bits - 1)
        sig = np.round(sig)
        sig = np.array(sig).astype(int)
        print(sig)
        quantized_coeffs.append(sig%16)
    quantized_coeffs = np.array(quantized_coeffs)

    print(quantized_coeffs)


    return  quantized_coeffs
    #quant = np.binary_repr(data/bits*8)


    #for i in range(len(data)):
    #    auxData.append(data[i])
    #return np.array(auxData)
'''