import numpy as np
from obstacle import obstacle
import matplotlib.pyplot as plt
import matplotlib

def plot(dis, disLine, tau):
    '''
        This function makes the visualization of the simulation box, which involves the
        obstacle array points and dislocation line and saves them in .jpeg format
        
        Variables that can be changed:
        -size (size of the obstacle points)
        -col (color of the obstacle points)
        -thick (thickness of the dislocation line)
        -discolor (color of the dislocation line)
        -dpival (dpi or resolution of the image [high values will increase the size of the image])
        
    '''
    size     = 25
    col      = 'lawngreen'
    thick    = 2.5
    discolor ='r'
    dpival   = 550
    lwidth   = 0.55
    
    array1 = np.array([[obs.x, obs.y] for obs in obstacle.array])
    plt.scatter(array1[:,0], array1[:,1], s=size, c=col, edgecolor='black', linewidths=lwidth)
    
    for segment in disLine:
        xs = [x for x, y in segment]
        ys = [y for x, y in segment]
        plt.plot(xs, ys, c=discolor, lw=thick)
    
    array2 = np.array([[obs.x, obs.y] for obs in dis])
    plt.scatter(array2[:,0], array2[:,1], s=size, c=col, edgecolor=discolor, linewidths=lwidth)
    
    #title = "\u03C4 = "+str(tau)
    #plt.suptitle(title, fontsize = 30)
    
    plt.gcf().set_size_inches((10, 10)) 
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    plt.yticks([]) 
    plt.xticks([]) 
    
    name = str((round(tau, 4)))+'.jpg'
    plt.savefig(name, dpi=dpival)
    plt.close()
