import numpy as np
from obstacle import obstacle
import matplotlib.pyplot as plt
import matplotlib

def plot(dis, disLine, tau, theta1, theta2):
    '''
        This function makes the visualization of the simulation box, which involves the
        obstacle array points and dislocation line and saves them in .jpeg format
        
        Variables that can be changed:
        -size (size of the obstacle points)
        -color1 & color2 (colors of the obstacles points in set1 and set2)
        -thick (thickness of the dislocation line)
        -discolor (color of the dislocation line)
        -dpival (dpi or resolution of the image [high values will increase the size of the image])
        
    '''
    size= 40
    color1= 'dodgerblue'
    color2= 'springgreen'
    thick= 2.5
    discolor='red'
    dpival = 350
    
    array1 = np.array([[obs.x, obs.y] for obs in obstacle.array if obs.brAngle==theta1])
    array2 = np.array([[obs.x, obs.y] for obs in obstacle.array if obs.brAngle==theta2])
    
    plt.scatter(array1[:,0], array1[:,1], s=size, c=color1, edgecolor='black', linewidths=1)
    plt.scatter(array2[:,0], array2[:,1], s=size, c=color2, edgecolor='black', linewidths=1)
    
    for segment in disLine:
        xs = [x for x, y in segment]
        ys = [y for x, y in segment]
        plt.plot(xs, ys, c=discolor, lw=thick)
    
    array3 = np.array([[obs.x, obs.y] for obs in dis if obs.brAngle==theta1])
    array4 = np.array([[obs.x, obs.y] for obs in dis if obs.brAngle==theta2])
    
    if len(array3)!=0:
        plt.scatter(array3[:,0], array3[:,1], s=size, c=color1, edgecolor=discolor, linewidths=1)
    if len(array4)!=0:
        plt.scatter(array4[:,0], array4[:,1], s=size, c=color2, edgecolor=discolor, linewidths=1)
    
    #title = "\u03C4 = "+str(tau)
    #plt.suptitle(title, fontsize = 30)
    
    plt.gcf().set_size_inches((9, 9)) 
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    plt.yticks([]) 
    plt.xticks([]) 
    
    name = str((round(tau, 4)))+'.jpg'
    plt.savefig(name, dpi=dpival)
    plt.close()   