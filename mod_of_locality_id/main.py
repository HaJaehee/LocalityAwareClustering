"""
 File name : mod_of_locality_id/main.py
 Author : Jaehee Ha (jaehee.ha@kaist.ac.kr)
 Creation Date : 2021-06-04
 Version : 1.0.1
 Created this module.

  Rev. history : 2021-06-06
 Version : 1.0.1
 Implementation is ongoing.
 Modifier : Jaehee ha (jaehee.ha@kaist.ac.kr)
"""

import os

def main():
    clustered_file = open("../korea-100-router-centroid-list.txt", 'r')
    id_replacement_file = open("../korea-100-router-clustered-id-rep.imn", 'w')
    centroid_list_file = open("../korea-100-router-centroid-list.txt", 'r')
    centroid_list = []

    while True :
        line = centroid_list_file.readline()
        if not line : break
        centroid_list.append(line.split(","))
    centroid_list_file.close()

    path_dir = "./latencies"
    file_list = os.listdir(path_dir)

    for file in file_list :
        for centroid in centroid_list :
            if centroid[0]+centroid[1] == file.replace("-latencies.txt", ""): continue
        latency_file = open(path_dir+"/"+file, 'r')
        while True :
            line = latency_file.readline()
            if not line : break
            lowest_latency = 100
            lowest_latency_ip = str()
            if "icmp_seq=5" in line :
                line_split = line.split(" ")
                if lowest_latency > line_split[6].replace("time=", ""):
                    lowest_latency = line_split[6].replace("time=", "")
                    lowest_latency_ip = line_split[3].replace(":", "")
        latency_file.close()
        



if __name__ == "__main__" :
    main ()