# This is a sample Python script.

"""
 File name : main.py
 Author : Jaehee Ha (jaehee.ha@kaist.ac.kr)
 Creation Date : 2021-06-01
 Version : 0.0.1
 Created this module.
 Implemented 2-mean clustering algorithm for edge nodes.

 Rev. history : 2021-06-03
 Version : 1.0.0
 First approach implementation is done.
 Modifier : Jaehee ha (jaehee.ha@kaist.ac.kr)

"""

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
import math
import scipy as sp
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import re

__result_list__=[]
__result_label__=0

def main():
    # Use a breakpoint in the code line below to debug your script.
    coordinate_list = []
    coordinate_list_with_name = []

    imn_file = open("korea-100-router.imn", 'r')
    node_name = str()
    while True:
        line = imn_file.readline()
        if not line: break

        if "node" in line:
            if "nodes" not in line:
                node_name = line.split(" ")[1]
        if "iconcoords" in line:
            x = line.split("{")[1].split(" ")[0]
            y = line.split("{")[1].split(" ")[1].split("}")[0]

            coords = list([float(x), float(y)])
            coords2 = list([node_name, float(x), float(y)])
            coordinate_list.append(coords)
            coordinate_list_with_name.append(coords2)
    imn_file.close()

    #print(coordinate_list)
    #print(coordinate_list_with_name)

    X=np.array(coordinate_list[:])
    #print(X[:,0])
    #print(X[:,1])
    #plt.scatter(X[:, 0], X[:, 1])
    #plt.show()

    level=int(5)

    #kmeans = KMeans(n_clusters=16)
    #kmeans.fit(X)
    #print(kmeans.cluster_centers_)
    #print(kmeans.labels_)

    #plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap='rainbow')
    #plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='black')
    #plt.show()

    two_means_cluster(X, level)

    global __result_list__
    #print (__result_list__)

    coordinate_list_with_name_n_label=[]
    idx_i=0
    for i in __result_list__:
        idx_j=0
        for j in coordinate_list_with_name:
            if j[1] == i[0] and j[2] == i[1]:
                coordinate_list_with_name_n_label.append([j[0], j[1], j[2], bin(i[2]).split("b")[1].zfill(5), i[3]])
                del coordinate_list_with_name[idx_j]
            idx_j += 1
        idx_i += 1

    coordinate_list_with_name_n_label.sort(key=lambda x:x[1])

    #print("\n\n")
    #print(coordinate_list_with_name_n_label)

    node_list_file = open("korea-100-router-node-list.txt", 'w')
    for i in coordinate_list_with_name_n_label :
        node_list_file.write(str(i[3])+","+bin(int(i[0].split("n")[1])).split("b")[1].zfill(10)+","+str(i[0])+","+str(i[1])+","+str(i[2])+","+str(i[4])+","+"\n")
    node_list_file.close()

    imn_file = open("korea-100-router.imn", 'r')

    imn_file2 = open("korea-100-router-clustered.imn", 'w')

    while True:
        line = imn_file.readline()
        if not line: break

        for i in coordinate_list_with_name_n_label:
            if "nodes" in line :
                line_split = line.split(" ")
                if str("{"+i[0]) == line_split[5] :
                    line_split[5] = "{"+i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(10)
                if str(i[0]+"}\n") == line_split[6] :
                    line_split[6] = i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(10)+"}\n"
                line = "    "+line_split[4]+" "+line_split[5]+" "+line_split[6]

            elif "node" in line :
                line_split = line.split(" ")
                if i[0] == line_split[1] :
                    line_split[1] = i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(10)
                line = line_split[0]+" "+line_split[1]+" "+line_split[2]

            elif "hostname" in line:
                line_substr = line[10:]
                if str(i[0]+"\n") == line_substr :
                    line_substr = i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(10)+"\n"
                line = "\thostname "+line_substr

            elif "interface-peer" in line:
                line_split = line.split(" ")
                if str(i[0]+"}\n") == line_split[6]:
                    line_split[6] = i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(10)+"}\n"
                line = "    "+line_split[4]+" "+line_split[5]+" "+line_split[6]
        imn_file2.write(line)
    imn_file.close()
    imn_file2.close()



def two_means_cluster(array_x, level):
    if level == 0:
        return
    global __result_list__
    global __result_label__
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(array_x)
    a = []
    b = []
    idx = 0
    idx_minimum_a = 0
    minimum_dist_a = 0
    minimum_dist_temp_a = 10000000
    idx_minimum_b = 0
    minimum_dist_b = 0
    minimum_dist_temp_b = 10000000
    for i in array_x:
        if kmeans.labels_[idx] == 0:
            a.append(i)
            if level == 1:
                minimum_dist_a = ((i[0]-kmeans.cluster_centers_[0][0]) ** 2) + ((i[1]-kmeans.cluster_centers_[0][1]) ** 2)
                if minimum_dist_a < minimum_dist_temp_a :
                    if len(__result_list__) > 0 :
                        __result_list__[idx_minimum_a][3] = ''
                    __result_list__.append([i[0], i[1], __result_label__, 'centroid'])
                    idx_minimum_a = len(__result_list__) - 1
                    minimum_dist_temp_a = minimum_dist_a
                else :
                    __result_list__.append([i[0], i[1], __result_label__, ''])

        elif kmeans.labels_[idx] == 1:
            b.append(i)
            if level == 1:
                minimum_dist_b = ((i[0]-kmeans.cluster_centers_[1][0]) ** 2) + ((i[1]-kmeans.cluster_centers_[1][1]) ** 2)
                if minimum_dist_b < minimum_dist_temp_b :
                    if len(__result_list__) > 0 :
                        __result_list__[idx_minimum_b][3] = ''
                    __result_list__.append([i[0], i[1], __result_label__, 'centroid'])
                    idx_minimum_b = len(__result_list__) - 1
                    minimum_dist_temp_b = minimum_dist_b
                else :
                    __result_list__.append([i[0], i[1], __result_label__+1, ''])
        idx += 1
    level -= 1
    np_a = np.array(a[:])
    np_b = np.array(b[:])
    if level == 0:
        #print (np_a)
        #print (np_b)
        #print (kmeans.cluster_centers_)
        __result_label__ += 1

    two_means_cluster(np_a, level)
    two_means_cluster(np_b, level)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
