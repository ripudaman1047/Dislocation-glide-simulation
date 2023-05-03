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

    arrsize = get_int("Number of obsatcles: ", errstr, Min=0)
    disttype = get_int("Choose type of strength distribution: (Enter '0' or '1')\n [0]Normal\n [1]Log-normal\n>>", errstr, Min=-1, Max=2)

    if disttype==0:
        
        mu = get_float("Mean strength of obstacles: ", errstr, Min=0, Max=1)    
        sigma = get_float("Standard deviation: ", errstr, Min=0, Max=1)
        
        dist = np.random.normal(mu, sigma, arrsize)
            
        new_dist = []
        for obsStrength in dist:
            if obsStrength > 1:
                new_dist.append(0.999)
            elif obsStrength < 0:
                new_dist.append(0.001)
            else:
                new_dist.append(obsStrength)
        
    if disttype==1:
        
        mu = get_float("Mean strength of obstacles: ", errstr, Min=0, Max=1)    
        sigma = get_float("Standard deviation: ", errstr, Min=0, Max=1)

        sigma_norm = np.sqrt(np.log(1 + (sigma/mu)**2))
        mu_norm = np.log(mu) - 0.5*sigma_norm**2
        
        dist = np.random.lognormal(mu_norm, sigma_norm, arrsize)
        new_dist = []
        for obsStrength in dist:
            if obsStrength > 1:
                new_dist.append(0.999)
            else:
                new_dist.append(obsStrength)
        
        
    breakangles = np.rad2deg(2*np.arccos(new_dist))

    initial= get_float("Enter the initial stress value: ", errstr, Min=1e-5)
    step = get_float("Enter the stress increment value: ", errstr, Min=1e-5, Max=0.1)
    imageflag = get_int("Image output at stable configurations(ON=1 / OFF=0): ", errstr, Min=-1, Max=2)

    xy_coords = np.random.rand(arrsize,2)

    obsarr = np.column_stack(((xy_coords, breakangles)))

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

    #################################################################
    with open('results.txt', 'w') as f:
        f.write("Random array size= {0}\n".format(arrsize))
        f.write("Stress increment size= {0}\n".format(step))
        f.write("Mean strength of obstacles= {0}\n".format(mu))
        f.write("Standard deviation= {0}\n".format(sigma))
        f.write("CRSS= {0}".format(CRSS))
        
    with open('stressstrain.csv', 'w', newline='') as g:  
        w = csv.writer(g)
        for row in zip(stressVstrain.values(), stressVstrain.keys()):
            w.writerow(row)

    if disttype==0:
        obs_name = str(arrsize)+"-Normal("+str(mu)+", "+str(sigma)+").csv"
    if disttype==1:   
        obs_name = str(arrsize)+"-Lognormal("+str(mu)+", "+str(sigma)+").csv"

    np.savetxt(obs_name, obsarr, delimiter = ",")

    current = str(dt.now().strftime("%d%m_%H%M%S"))
    src_dir = os.getcwd()
    dst_dir = src_dir+'\\results_'+obs_name[:-4]+"_"+current
    os.mkdir(dst_dir)

    shutil.move(os.path.join(src_dir, obs_name), dst_dir)
    shutil.move(src_dir+'\\results.txt', dst_dir)
    shutil.move(src_dir+'\\stressstrain.csv', dst_dir)

    if imageflag==1: 
        for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
            shutil.move(jpgfile, dst_dir)
            
    print("*****Result files created*****")

if __name__=="__main__":
    main()
    