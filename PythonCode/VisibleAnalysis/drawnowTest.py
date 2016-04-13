from pylab import arange, plt
from drawnow import drawnow
import numpy as np

plt.ion() # enable interactivity

def makeFig():
    plt.plot(x,y) # I think you meant this

x=list()
y=list()

for i in arange(100):
    x = [0]
    y = [0] # or any arbitrary update to your figure's data
    drawnow(makeFig)
    plt.pause(0.001)
