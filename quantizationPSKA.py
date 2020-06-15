import numpy as np

def quantization(data, nQuantBits, verbose=False):
    if verbose == True: print("\nQUANTIZAÇÃO - START")
    
    # Definindo limite superior e inferior dos dados a serem quantizados
    vMax = max(data)
    vMin = min(data)

    # Criação de uma lista vazia para armazenar os coeficientes quantizados
    quantized_coeffs = []

    # Definindo o número de níveis de acordo com a quantidade de bits
    nLevels = 2^nQuantBits

    # Definindo distância entre os níveis
    distLevels = (vMax-vMin)/nLevels

    # Quantização de cada um dos valores da lista de dados 
    for key in data:
        level = 0
        limiar = vMin+(level+1)*distLevels
        while(key > limiar and limiar < vMax):
            level = level + 1
            limiar = vMin+(level+1)*distLevels
        quantized_coeffs.append(level)
    
    #quantized_coeffs = np.array(quantized_coeffs)

    if verbose == True:
        print("\nDados:")
        print(data)
        print("\nDados Quantizados:")
        print(quantized_coeffs)
        print("\nQUANTIZAÇÃO - END\n")
    
    return quantized_coeffs