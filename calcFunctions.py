import numpy as np 
import pandas as pd 

#usefulFunction

def LSEfficiency(miu, lead, diameter): # miu [], lead [mm/rev], diameter [mm]

    r = diameter/2 # [mm]
    alpha = np.arctan(lead/(2*np.pi*r))
     
    effLS = (1-miu*np.tan(alpha))/(1+miu*(1/np.tan(alpha)))
    return effLS


def LSEfficiencyACME(miu, lead, diameter, lamda):
    r = diameter/2 # [mm]
    alpha = np.arctan(lead/(2*np.pi*r)) #calculate alpha
    #calculate lamda

    effLSNum = np.cos(lamda)-miu*np.tan(alpha)
    effLSDen = np.cos(lamda)+miu*(1/np.tan(alpha))

    effLS = effLSNum/effLSDen
    return effLS
