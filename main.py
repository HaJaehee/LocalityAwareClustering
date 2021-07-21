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

 Rev. history : 2021-06-13
 Version : 1.0.1
 Node num and ip list extraction is implemented.
 Modifier : Jaehee ha (jaehee.ha@kaist.ac.kr)

 Rev. history : 2021-07-15
 Version : 1.1.0
 Added clustering scheme based on cluster weights.
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

def main2():
    node_list_file = open("korea-100-router-node-list.txt", 'r')
    node_num_ip_file = open("korea-100-router-node-num-ip-list.txt", 'w')
    node_num_ip_list = []
    while True:
        line = node_list_file.readline()
        if not line: break
        line_split = line.split(",")
        node_num_ip_list.append((line_split[3].replace("n", "").zfill(3), line_split[2]))

    node_list_file.close()
    sorted_list = sorted(node_num_ip_list, key=lambda x:x[0])

    for i in sorted_list :
        node_num_ip_file.write(i[0]+","+i[1]+"\n")

    node_num_ip_file.close()

def main():
    # Clusters nodes from file 'imn_file' and outputs file 'imn_file2'

    coordinate_list = []
    coordinate_list_with_name_ip = []

    imn_file = open("korea-37-router.imn", 'r')
    node_name = str()
    ip_address = str()
    while True:
        line = imn_file.readline()
        if not line: break

        if "hostname" in line:
            node_name = line.split(" ")[1].replace("\n", "")
        if "interface eth0" in line:
            line = imn_file.readline()
            if "ip address" in line:
                ip_address = line[13:].replace("\n", "")
        if "iconcoords" in line:
            x = line.split("{")[1].split(" ")[0]
            y = line.split("{")[1].split(" ")[1].split("}")[0]

            coords = list([float(x), float(y)])
            coords2 = list([node_name, float(x), float(y), ip_address])
            coordinate_list.append(coords)
            coordinate_list_with_name_ip.append(coords2)
    imn_file.close()

    #print(coordinate_list)
    #print(coordinate_list_with_name_ip)

    #X=np.array(coordinate_list[:])
    X = pd.DataFrame(np.array(coordinate_list[:]), columns=['x','y'])
    #print(X[:,0])
    #print(X[:,1])
    #plt.scatter(X[:, 0], X[:, 1])
    #plt.show()


    # ks = range(1, 10)
    # inertias = []
    # for k in ks:
    #     model = KMeans(n_clusters=k)
    #     model.fit(X)
    #     inertias.append(model.inertia_)
    # plt.plot(ks, inertias, '-o')
    # plt.xlabel('number of clusters, k')
    # plt.ylabel('inertia')
    # plt.xticks(ks)
    # plt.show()

    # print(X)
    n_clusters = 13
    kmeans = KMeans(n_clusters=n_clusters)
    condition = 5
    # A cluster size MUST be equal or lower than condition
    while True:
        node_count = []
        for i in range(0, n_clusters):
            node_count.append(0)
        kmeans.fit(X)
        is_continue = False
        for i in kmeans.labels_:
            node_count[i] += 1
            if node_count[i] > condition:
                is_continue = True
                break
        if is_continue is True:
            continue
        else:
            break

    #print(kmeans.cluster_centers_)
    #print(kmeans.labels_)

    # Replace labels based on distance from zero point
    new_cluster_centers_ = []
    dist = []
    inc = 0
    for i in kmeans.cluster_centers_:
        dist.append([(i[0] ** 2) + (i[1] ** 2), inc])
        new_cluster_centers_.append([])
        inc += 1

    dist.sort(key=lambda x:x[0])
    #print(dist)

    old_new_label_map = {}
    inc = 0
    for old_label in dist:
        old_new_label_map[old_label[1]] = inc
        inc += 1
    #print (old_new_label_map)

    new_labels_ = []
    for old_label in kmeans.labels_:
        new_labels_.append(old_new_label_map[old_label])
    for i in range(0, n_clusters) :
        new_cluster_centers_[old_new_label_map[i]] = kmeans.cluster_centers_[i]

    #print(new_cluster_centers_)
    #print(new_labels_)

    X['label'] = np.array(new_labels_[:])

    #plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap='rainbow')
    sns.scatterplot(x="x", y="y", hue="label", data=X, palette="rainbow", legend='full')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='black')
    plt.legend()
    plt.show()

    #level = int(4)
    #two_means_cluster(X, level)

    global __result_list__

    # New chose centroids
    idx_minimum = {}
    minimum_dist = {}
    minimum_dist_temp = {}
    for idx, row in X.iterrows():
        # row['x'], row['y'], row['label']
        # new_labels_
        # new_cluster_centers_
        # distance calculation
        # x-axis: row['x'], new_cluster_centers_[row['label']][0]
        # y-axis: row['y'], new_cluster_centers_[row['label']][1]
        x = row['x']
        y = row['y']
        label = int(row['label'])
        minimum_dist_temp[label] = ((x - new_cluster_centers_[label][0]) ** 2) + ((y - new_cluster_centers_[label][1]) ** 2)
        if not label in minimum_dist:
            __result_list__.append([x, y, label, 'centroid'])
            idx_minimum[label] = len(__result_list__)-1
            minimum_dist[label] = minimum_dist_temp[label]
        elif minimum_dist[label] > minimum_dist_temp[label]:
            if len(__result_list__) > 0:
                __result_list__[idx_minimum[label]][3] = ''
            __result_list__.append([x, y, label, 'centroid'])
            idx_minimum[label] = len(__result_list__)-1
            minimum_dist[label] = minimum_dist_temp[label]
        else:
            __result_list__.append([x, y, label, ''])
    print(__result_list__)


    coordinate_list_with_name_label_ip=[]
    idx_i=0
    for i in __result_list__:
        idx_j=0
        for j in coordinate_list_with_name_ip:
            if j[1] == i[0] and j[2] == i[1]:
                coordinate_list_with_name_label_ip.append([j[0], j[1], j[2], bin(i[2]).split("b")[1].zfill(5), i[3], j[3]])
                del coordinate_list_with_name_ip[idx_j]
            idx_j += 1
        idx_i += 1

    coordinate_list_with_name_label_ip.sort(key=lambda x:x[1])

    #print("\n\n")
    #print(coordinate_list_with_name_label_ip)

    node_list_file = open("korea-37-router-node-list.txt", 'w')
    centroid_list_file = open("korea-37-router-centroid-list.txt", 'w')
    centroid_ip_list_file = open("korea-37-router-centroid-ip-list.txt", 'w')
    for i in coordinate_list_with_name_label_ip :
        if "centroid" in i[4]:
            centroid_list_file.write(str(i[3])+","+bin(int(i[0].split("n")[1])).split("b")[1].zfill(8)+","+str(i[5])+","+str(i[0])+","+str(i[1])+","+str(i[2])+","+str(i[4])+"\n")
            centroid_ip_list_file.write(str(i[5]).replace("/24", "")+"\n")
        node_list_file.write(
            str(i[3]) + "," + bin(int(i[0].split("n")[1])).split("b")[1].zfill(8) + "," + str(i[5]) + "," + str(
                i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[4]) + "\n")

    centroid_list_file.close()
    centroid_ip_list_file.close()
    node_list_file.close()

    imn_file = open("korea-37-router.imn", 'r')

    imn_file2 = open("korea-37-router-clustered.imn", 'w')

    while True:
        line = imn_file.readline()
        if not line: break

        for i in coordinate_list_with_name_label_ip:
            """
            if "nodes" in line :
                line_split = line.split(" ")
                if str("{"+i[0]) == line_split[5] :
                    line_split[5] = "{"+i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(8)
                if str(i[0]+"}\n") == line_split[6] :
                    line_split[6] = i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(8)+"}\n"
                line = "    "+line_split[4]+" "+line_split[5]+" "+line_split[6]

            elif "node" in line :
                line_split = line.split(" ")
                if i[0] == line_split[1] :
                    line_split[1] = i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(8)
                line = line_split[0]+" "+line_split[1]+" "+line_split[2]
            """
            if "hostname" in line:
                line_substr = line[10:]
                if str(i[0]+"\n") == line_substr :
                    line_substr = i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(8)+"\n"
                line = "\thostname "+line_substr
            """
            elif "interface-peer" in line:
                line_split = line.split(" ")
                if str(i[0]+"}\n") == line_split[6]:
                    line_split[6] = i[3]+bin(int(i[0].split("n")[1])).split("b")[1].zfill(8)+"}\n"
                line = "    "+line_split[4]+" "+line_split[5]+" "+line_split[6]
            """
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
            if level == 1 :
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
            if level == 1 :
                minimum_dist_b = ((i[0]-kmeans.cluster_centers_[1][0]) ** 2) + ((i[1]-kmeans.cluster_centers_[1][1]) ** 2)
                if minimum_dist_b < minimum_dist_temp_b :
                    if len(__result_list__) > 0 :
                        __result_list__[idx_minimum_b][3] = ''
                    __result_list__.append([i[0], i[1], __result_label__+1, 'centroid'])
                    idx_minimum_b = len(__result_list__) - 1
                    minimum_dist_temp_b = minimum_dist_b
                else :
                    __result_list__.append([i[0], i[1], __result_label__+1, ''])
        idx += 1
    level -= 1
    np_a = np.array(a[:])
    np_b = np.array(b[:])
    if level == 0:
        #print ('np_a')
        #print (np_a)
        #print ('np_b')
        #print (np_b)
        #print (kmeans.cluster_centers_)
        __result_label__ += 1

    two_means_cluster(np_a, level)
    two_means_cluster(np_b, level)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
