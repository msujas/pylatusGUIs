import numpy as np
import matplotlib.pyplot as plt
import sys,re
from scipy.optimize import curve_fit
import argparse


file = sys.argv[1]

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='TCal file name to plot')
    args = parser.parse_args()
    file = args.file
    return file

def run():
    file = parseArgs()
    Tset,Tmeas,Terr = np.loadtxt(file,unpack = True,usecols = (0,1,2),skiprows = 8)

    Tsetmaxi = np.abs(Tset-max(Tset)).argmin()

    f = open(file,'r')
    lines = f.readlines()

    a0 = float(re.split('[=+]',[line for line in lines if '#a0' in line][0])[1])
    a1 = float(re.split('[=+]',[line for line in lines if '#a1' in line][0])[1])
    a2 = float(re.split('[=+]',[line for line in lines if '#a2' in line][0])[1])
    Tseries = np.arange(0,1200)
    Tfit = a0 + a1*Tseries + a2*Tseries**2
    fitstring = f'Tcal = {a0:.5f} + {a1:.5f}*Tmeas\n+ {a2:.5e}*Tmeas^2'

    def quad_fit(x,a0,a1,a2):
        return a0 + a1*x + a2*x**2
    Terr[0] = 0.01

    popt,pcov = curve_fit(quad_fit,Tset[:Tsetmaxi+1],Tmeas[:Tsetmaxi+1],sigma = Terr[:Tsetmaxi+1])
    fitstring2 = f'Tcal2 = {popt[0]:.5f} + {popt[1]:.5f}*Tmeas\n+ {popt[2]:.5e}*Tmeas^2'
    Tfit2 = quad_fit(Tseries,*popt)

    minx = min(Tset)-(max(Tset)-min(Tset))*0.1
    maxx = max(Tset)+(max(Tset)-min(Tset))*0.1
    plt.errorbar(Tset,Tmeas,Terr,capsize = 3,fmt='o-',label = 'measured')
    plt.plot(Tseries,Tfit,label = 'fit')
    plt.plot(Tseries,Tfit2,label = 'fit2 (fixed RT)')
    plt.xlim(minx,maxx)
    plt.xlabel('Tset (°C)')
    plt.ylabel('Tmeas (°C)')
    plt.annotate(fitstring,xy = ((maxx+minx)*0.5,max(Tfit)*0.1))
    plt.annotate(fitstring2,xy = ((maxx+minx)*0.5,max(Tfit)*0.01))
    plt.legend()
    plt.title(file)
    plt.show()
