from functions import *
def main():
    from obstacle import obstacle
    from inputfunc import get_float, get_int
    from visual import plot
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.spatial import KDTree
    from datetime import datetime as dt
    import random
    import glob
    import shutil
    import csv
    import os

    errstr = "Invalid response! Try again"

    arrsize= get_int("Number of obsatcles: ", errstr, Min=0)
    val= get_float("Breaking angle(in degrees): ", errstr, Min=0, Max=180)
    initial= get_float("Enter the initial stress value: ", errstr, Min=1e-5)
    step= get_float("Enter the stress increment value(1e-5 to 1e-1): ", errstr, Min=0.99e-5, Max=0.105)
    imageflag= get_int("Image output at stable configurations(ON=1 / OFF=0): ", errstr, Min=-1, Max=2)

    xy_coords = np.random.rand(arrsize,2)
    dist = np.array([val]*arrsize)
    obsarr = np.column_stack(((xy_coords, dist)))

    for i in range(len(obsarr)):
        obstacle(x=obsarr[i][0], y=obsarr[i][1], brAngle=obsarr[i][2])

    tau = initial
    ls = np.sqrt(1/len(obstacle.array))
    R = 0.5/tau
    rNorm = R*ls

    os.system('cls')

    ObsTree = KDTree(np.array([[obs.x, obs.y] for obs in obstacle.array])) 

    dis = []
    stressVstrain = {}
    while not dis == None:
        dis = initial_segment(rNorm)
        if dis == None:
            CRSS = round(tau-step,6)
            print("Critical resolved shear stress \u03C4 =", CRSS)
            break
        
        while not dis[-1].x > 1:
            area = swept_ar(dis[-1], rNorm, ObsTree)
            
            if 1-dis[-1].x < rNorm:
                area.append(obstacle(x=2-dis[-1].x, y=dis[-1].y, brAngle=dis[-1].brAngle))
            
            if len(area)==0:
                dis[-1].mk_invisible()
                dis.remove(dis[-1])
            
            else:
                addPt = circle_roll(dis[-1], dis, area, rNorm)
                if addPt is None:
                    dis[-1].mk_invisible()
                    dis.remove(dis[-1])
                else:
                    dis.append(addPt)
                    addPt.mk_invisible()
                    
            if len(dis) == 1:
                dis[0].mk_invisible()
                dis.remove(dis[0])
                dis = initial_segment(rNorm)
                if dis == None:
                    break
            
            if dis[-1].y > 0.95:
                dis = None
                break
        
        if dis == None:
            CRSS = round(tau-step,6)
            print("Critical resolved shear stress \u03C4 =", CRSS)
            break
        else:
            print(" \u03C4 = {}".format(tau))
        
        if imageflag==1:
            disLine = dislocation_segment(dis, rNorm)
            plot(dis, disLine, tau)
        
        area_under_line(dis, stressVstrain, tau)
        reset(dis)
        
        tau = round(tau+step,6)
        R = 0.5/tau
        rNorm = R*ls
    ############################################################

    with open('results.txt', 'w') as f:
        f.write("Random array size= {0}\n".format(arrsize,))
        f.write("Breaking angle= {0}\n".format(val))
        f.write("Stress increment= {0}\n".format(step))
        f.write("CRSS= {0}\n".format(CRSS))
        
    with open('stressstrain.csv', 'w', newline='') as g:  
        w = csv.writer(g)
        for row in zip(stressVstrain.values(), stressVstrain.keys()):
            w.writerow(row)

    obs_name = str(arrsize)+"-"+str(val)+".csv"
    np.savetxt(obs_name, obsarr, delimiter = ",")

    current = str(dt.now().strftime("%d%m_%H%M%S"))
    src_dir = os.getcwd()
    dst_dir = src_dir+'\\results_'+obs_name[:-4]+"_"+current
    os.mkdir(dst_dir)

    shutil.move(src_dir+'\\results.txt', dst_dir)
    shutil.move(src_dir+'\\stressstrain.csv', dst_dir)
    shutil.move(os.path.join(src_dir, obs_name), dst_dir)

    if imageflag==1: 
        for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
            shutil.move(jpgfile, dst_dir)
            
    print("*****Result files created*****")

if __name__=="__main__":
    main()
    
