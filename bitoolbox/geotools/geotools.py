# -*- coding: utf-8 -*-
def get_lat_lon(p):
    if(type(p) is str):
        p = [x.strip() for x in p.split(',')]

    if(type(p) is tuple or type(p) is list):
        if(len(p) != 2):
            raise ValueError("Point need to have 2 values.")
        lat = float(p[0])
        lon = float(p[1])
    else:
        raise ValueError("Point is not the right type.")
    return lat, lon


def distance_latlon(p1, p2):
    
    # approximate radius of earth in km
    R = 6373.0
    

    lat1, lon1 = get_lat_lon(p1)      
    lat2, lon2 = get_lat_lon(p2)

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