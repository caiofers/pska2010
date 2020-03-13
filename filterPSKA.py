import numpy as np
import plotPSKA

def filterPSKA(data, max, min, verbose=False, plot=False):
    auxData = []
    for i in range(len(data)):
        if int(data[i]) < max and int(data[i]) > min:
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