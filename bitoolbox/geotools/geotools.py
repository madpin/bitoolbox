# -*- coding: utf-8 -*-

def distance_latlon(p1, p2):
    
    # approximate radius of earth in km
    R = 6373.0
    
    if(type(p1) is str):
        p1 = [x.strip() for x in p1.split(',')]

    if(type(p1) is tuple or type(p1) is list):
        if(len(p1) != 2):
            raise ValueError("Point 1 need to have 2 values.")
        lat1 = float(p1[0])
        lon1 = float(p1[1])

                     
    if(type(p2) is str):
        p2 = [x.strip() for x in p2.split(',')]

    if(type(p2) is tuple or type(p2) is list):
        if(len(p2) != 2):
            raise ValueError("Point 2 need to have 2 values.")
        lat2 = float(p2[0])
        lon2 = float(p2[1])

    from math import sin, cos, sqrt, atan2, radians

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c