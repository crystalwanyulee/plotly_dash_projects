# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 18:33:27 2020

@author: admin
"""

from math import sin, cos, sqrt, atan2, radians


def get_distance(lat1, lon1, lat2, lon2):
    R = 6370
    lat1 = radians(lat1)  #insert value
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2- lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance


def create_distance_file(city: list, lat: list, lon: list, path: str):
    dist = []
    
    for i in range(len(city)):
        city1, lat1, lon1 = city[i], lat[i], lon[i]
        
        for j in range(i+1, len(city)):
            city2, lat2, lon2 = city[j], lat[j], lon[j]
            d = get_distance(lat1, lon1, lat2, lon2)
            dist.append(', '.join([city1, city2, str(round(d))]))
               
    with open(path, "w") as f:
        f.write('\n'.join(dist))    
        


if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv('C://Users/admin/Documents/Python2/main/data/data.csv')
    df.head()


    path = 'C://Users/admin/Documents/Python2/main/data/city_dist.txt'
    create_distance_file(df['city'], df['latitude'], df['longtitude'], path)
    
    
