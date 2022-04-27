
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure



def print_plot(x,vec,img_path,title): 
   
    X_axis = np.arange(len(x))
    avg=[]
    min=[]
    max=[]
    for rows in vec:
        avg.append(rows[0])
        min.append(rows[1])
        max.append(rows[2])
    plt.rcParams.update({'font.size': 12})
    figure(figsize=(20,16), dpi=80)
    plt.bar(X_axis - 0.2, avg, 0.2, label = 'AVG')
    plt.bar(X_axis, min, 0.2, label = 'MIN')
    plt.bar(X_axis + 0.2, max, 0.2, label = 'MAX')
    plt.xticks(X_axis, x)
    plt.xlabel("projects")
    plt.ylabel("Complexity")
    plt.title(title)
    plt.legend()
    plt.savefig(img_path)
    plt.cla()
    return

def static_analysis(path_to_csvs,image_name):
    files = []
    avg= []
    min= []
    max= []
    for file in os.listdir(path_to_csvs):
        if file.endswith(".csv"):
            files.append(file)

    files.sort()
    for file in files:
        with open(path_to_csvs+"/"+file) as data:
            csvreader = csv.reader(data)
            header = next(csvreader)
            for row in csvreader:
                if row[0] == 'AVG':
                    avg.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                if row[0] == 'MIN':
                    min.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                if row[0] == 'MAX':
                    max.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
    x=[]
    for f in files:
        no_ext_f = f[:len(f) - 4]
        x.append(no_ext_f)

    sifis=[]
    sifis_q=[]
    crap=[]
    skunk=[]
    for i in range(len(avg)):
        sifis.append( [avg[i][0], min[i][0], max[i][0]])
        sifis_q.append( [avg[i][1], min[i][1], max[i][1]])
        crap.append( [avg[i][2], min[i][2], max[i][2]])
        skunk.append( [avg[i][3], min[i][3], max[i][3]])
    print_plot(x,sifis,'./img/'+image_name+'_sifis.png',"Sifis")
    print_plot(x,sifis_q,'./img/'+image_name+'_sifis_quantized.png',"Sifis Quantized")
    print_plot(x,crap,'./img/'+image_name+'_crap.png',"CRAP")
    print_plot(x,skunk,'./img/'+image_name+'_skunk.png',"SkunkScore")
    return

static_analysis("./StaticAnalysis","static_analysis")