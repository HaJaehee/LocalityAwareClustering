# This is a sample Python script.

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

def main():
    # Use a breakpoint in the code line below to debug your script.
    l = []
    f = open("korea-100-router.imn", 'r')

    while True:
        line = f.readline()
        if not line: break
        if "iconcoords" in line:
            print(line)
            x = line.split("{")[1].split(" ")[0]
            y = line.split("{")[1].split(" ")[1].split("}")[0]

            coords = list([float(x),float(y)])
            l.append(coords)
    f.close()

    print(l)

    X=np.array(l[:])
    #print(X[:,0])
    #print(X[:,1])
    #plt.scatter(X[:, 0], X[:, 1])
    #plt.show()

    kmeans = KMeans(n_clusters=32)
    kmeans.fit(X)
    print(kmeans.cluster_centers_)
    plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap='rainbow')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='black')
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
