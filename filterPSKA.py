import numpy as np
import plotPSKA

def filterPSKA(data, vMin, vMax, verbose=False, plot=False):
    # Criação de uma lista vazia para adicionar os dados filtrados
    auxData = []
    for i in range(len(data)):
        if int(data[i]) < vMax and int(data[i]) > vMin:
            # Se o dado estiver entre o máximo e míno pré-estabelecido, o valor é adicionado à lista de dados filtrados
            auxData.append(data[i])
    
    if verbose:
        print("\nDados sem filtro: ")
        print(data)
        print("\nDados filtrados: ")
        print(np.array(auxData))
    
    if plot:
        plotPSKA.plot('Sample', 'Signal', data, filtered=False)
        plotPSKA.plot('Sample', 'Signal w/ Filter', np.array(auxData))
    
    return np.array(auxData)