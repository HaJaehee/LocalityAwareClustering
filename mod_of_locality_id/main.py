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

  Rev. history : 2021-06-09
 Version : 1.0.2
 Id replacement code is implemented.
 Modifier : Jaehee ha (jaehee.ha@kaist.ac.kr)
"""

import os

def main():
    clustered_file = open("../korea-100-router-clustered.imn", 'r')
    id_replacement_file = open("../korea-100-router-clustered-id-rep.imn", 'w')
    centroid_list_file = open("../korea-100-router-centroid-list.txt", 'r')
    centroid_list = []
    centroid_ip_list = []
    while True :
        line = centroid_list_file.readline()
        if not line : break
        centroid_list.append(line.split(","))
        centroid_ip_list.append(centroid_list[len(centroid_list)-1][2])
    centroid_list_file.close()

    path_dir = "./latencies"
    file_list = os.listdir(path_dir)

    id_replacement_dic = {}

    for file in file_list :
        for centroid in centroid_list :
            if centroid[0]+centroid[1] == file.replace("-latencies.txt", ""): continue
        latency_file = open(path_dir+"/"+file, 'r')
        lowest_latency = 100.0
        lowest_latency_ip = str()
        while True :
            line = latency_file.readline()
            if not line : break
            if "icmp_seq=5" in line :
                line_split = line.split(" ")
                if lowest_latency > float(line_split[6].replace("time=", "")):
                    lowest_latency = float(line_split[6].replace("time=", ""))
                    lowest_latency_ip = line_split[3].replace(":", "")
        latency_file.close()
        centroid_list_idx = centroid_ip_list.index(lowest_latency_ip)
        old_locality_id = file.replace("-latencies.txt", "")
        new_locality_id = centroid_list[centroid_list_idx][0]+file.replace("-latencies.txt", "")[5:]
        print("old "+old_locality_id+" new "+new_locality_id)
        id_replacement_dic[old_locality_id] = new_locality_id

    while True :
        line = clustered_file.readline()
        if not line : break
        if line.startswith("\thostname") :
            old_locality_id = line[10:23]
            line = "\thostname " + id_replacement_dic[old_locality_id] + "\n"
        id_replacement_file.write(line)

    id_replacement_file.close()
    clustered_file.close()



if __name__ == "__main__" :
    main ()