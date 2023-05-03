import numpy as np
from obstacle import obstacle
import matplotlib.pyplot as plt


def get_center(p1, p2, radius):     
    '''
        This functions finds a circle's center coordinates with given radius,
        on whose circumfrence the two given points would lie.
    
        ===Parameters===
        p1, p2 : obstacle objects
        radius : float
        
        ===Ouput===
        cen : numpy array of coordinates of circle's center 
    '''
    q = np.sqrt((p2.x-p1.x)**2+(p2.y-p1.y)**2)
    x3 = (p1.x+p2.x)/2
    y3 = (p1.y+p2.y)/2

    xx = np.sqrt(radius**2-(q/2)**2)*((p1.y-p2.y)/q)
    yy = np.sqrt(radius**2-(q/2)**2)*((p2.x-p1.x)/q)
    
    both_centres = np.array([[x3+xx, y3+yy], [x3-xx, y3-yy]])
    
    vec1 = [p2.x-p1.x, p2.y-p1.y]
    vec2 = [both_centres[0][0]-p1.x, both_centres[0][1]-p1.y]
    vec3 = [both_centres[1][0]-p1.x, both_centres[1][1]-p1.y]
   
    if np.cross(vec1, vec2) < 0:
        return both_centres[0]
    else:
        return both_centres[1]

###############################################################################

def circle_roll(p1, dis, Area, rad):
    '''
        This functions selects the obstacle objects by circle rolling method to define a stable
        dislocation line.
        
        ===Parameters===
        p1 : obstacle object
        dis : list (consisting of the pre-existing points in the dislocation line)
        Area : list (consisting all the points around p1 within 2*rad distance)
        rad: float
        
        ===Output===
        newPt : obstacle object
    '''
    prevPt = dis[dis.index(p1)-1]
    vec1= get_center(prevPt, p1, rad)-p1.vector
    
    rot_dict = {}
    for point in Area:
        vec2= get_center(p1, point, rad)-p1.vector
        
        cosTh = np.dot(vec1,vec2)
        sinTh = np.cross(vec1,vec2)
        angle = np.rad2deg(np.arctan2(sinTh,cosTh))

        if angle <= 0:
            pos_angle = 360 + angle
        else:
            pos_angle = angle
        
        if pos_angle < 180-p1.brAngle:
            rot_dict[point] = pos_angle
    
    if len(rot_dict) == 0:
        return None
    else:
        newPt = min(rot_dict, key = rot_dict.get)
        return newPt

###############################################################################

def initial_segment(radius):
    '''
        This function returns a list of two obstacles which gets pinned by the dislocation on
        the left hand boundary of the obstacle plane. The stable radius corresponding the applied
        shear stress will define the search area for these two points.
        
        ===Parameters===
        radius : float
        
        ===Output===
        arr : list (contining two starting obstacle objects)
    '''
    arr = []
    temp = []
    for point in obstacle.array:
        if point.x < radius and point.y < 0.95 and point.is_visible:
            temp.append(point)
    if len(temp)==0:
        return None

    cen_dist = {}
    for point in temp:
        image = obstacle(x=-point.x, y=point.y, brAngle=point.brAngle)
        center = get_center(image, point, radius)
        cen_dist[point] = 1-(center[1])
        del image
    
    start = max(cen_dist, key = cen_dist.get)
    image = obstacle(x=-start.x, y=start.y, brAngle=start.brAngle)
    arr.append(image)
    arr.append(start)
    start.mk_invisible()
    image.mk_invisible()

    return arr

###############################################################################

# def swept_ar(p1, rad):
#     '''
#         This function gives all the obstacle points lying within a circle of radius 2*radius with
#         p1 as center.
        
#         ===Parameters===
#         p1 : obstacle object 
#         rad : float
        
#         ===Output===
#         arr : list
#     '''
#     arr = []     
#     for point in obstacle.array:
#         if np.sqrt((p1.x-point.x)**2+(p1.y-point.y)**2)<2*rad and point.is_visible and point!= p1:
#             arr.append(point)
#     return arr

def swept_ar(p1, rad, ObsTree):
    '''
        This function gives all the obstacle points lying within a circle of radius 2*radius with
        p1 as center
        
        ===Parameters===
        p1 : obstacle object
        rad : float
        
        ===Output===
        arr : list
    '''
    indices = ObsTree.query_ball_point([p1.x, p1.y], 2*rad) 
    
    arr = [obstacle.array[i] for i in indices if obstacle.array[i].is_visible and obstacle.array[i] != p1]
    return arr

###############################################################################

def reset(dis):
    '''
        Resets the program for the next run with different shrear stress.
    '''
    for point in obstacle.array:
        point.is_visible = True
    dis.clear()

###############################################################################

def dislocation_segment(dis, rNorm):
    '''
        This function makes the arc of the given radius between the selected
        points pinning the dislocation.
    '''
    theta1 = []
    theta2 = []
    for n in range(len(dis)-1):  
        line1 = dis[n].vector - get_center(dis[n], dis[n+1], rNorm) 
        line2 = dis[n+1].vector - get_center(dis[n], dis[n+1], rNorm) 
        v1_u = line1/np.linalg.norm(line1)
        v2_u = line2/np.linalg.norm(line2)
        angle1 =  np.math.atan2(np.linalg.det([v2_u,v1_u]),np.dot(v2_u,v1_u))
        theta1.append(angle1)

        line3 = dis[n+1].vector - get_center(dis[n], dis[n+1], rNorm) 
        line4 = [1,0]
        v3_u = line3/np.linalg.norm(line3)
        v4_u = line4/np.linalg.norm(line4)
        angle2 =  np.math.atan2(np.linalg.det([v4_u,v3_u]),np.dot(v4_u,v3_u))
        theta2.append(angle2)
    
    arr = []
    for d in range(len(dis)-1):
        arc_angles = np.linspace(theta2[d], theta2[d] + theta1[d], 40)
        arc_xs = get_center(dis[d], dis[d+1], rNorm)[0] + rNorm * np.cos(arc_angles)
        arc_ys = get_center(dis[d], dis[d+1], rNorm)[1] + rNorm * np.sin(arc_angles)
        arr.append(list(zip(arc_xs, arc_ys)))
    return arr

###############################################################################

def area_under_line(dis, stressVstrain, tau): 
    '''
        This function calculates the area under the dislocation line by numerical
        integration method (trapezoidal rule) corresponding to a stable
        dislocation configuration for shear stress tau.
    '''
    X, Y = [], []
    for point in dis[1:-1]:
        X.append(point.x)
        Y.append(point.y)
    X.append(1.0)
    Y.append(dis[-1].y)
    np.insert(X, 0, 0.0)
    np.insert(Y, 0, dis[0].y)
    
    area= np.trapz(Y, X)
    stressVstrain[tau] = area

###############################################################################

