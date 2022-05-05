
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure



def print_plot(x,vec,img_path,title): 
   
    X_axis = np.arange(len(x))
    avg_cyc= []
    max_cyc= []
    avg_cogn= []
    max_cogn= []
    for rows in vec:
        avg_cyc.append(rows[0])
        max_cyc.append(rows[2])
        avg_cogn.append(rows[1])
        max_cogn.append(rows[3])
    plt.rcParams.update({'font.size': 12})
    figure(figsize=(20,16), dpi=80)
    plt.bar(X_axis - 0.3, avg_cyc, 0.2, label = 'AVG Cyclomatic', color='#009302')
    plt.bar(X_axis - 0.1, max_cyc, 0.2, label = 'MAX Cyclomatic', color='#000FFF')
    plt.bar(X_axis + 0.1, avg_cogn, 0.2, label = 'AVG Cognitive', color='#00FF03')
    plt.bar(X_axis + 0.3, max_cogn, 0.2, label = 'MAX Cognitive', color='#747BF0')
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
    avg_cyc= []
    max_cyc= []
    avg_cogn= []
    max_cogn= []
    n_complex= []
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
                    if file.split("_")[1] == "cyc.csv":
                        avg_cyc.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                    else:
                        avg_cogn.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                if row[0] == 'MAX':
                     if file.split("_")[1] == "cyc.csv":
                        max_cyc.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                     else:
                        max_cogn.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                if row[0] == "TOTAL COMPLEX FILES":
                    n_complex.append(float(row[1]))
    x=[]
    for f in files:
        no_ext_f = f[:len(f) - 4]
        split_m = no_ext_f.split("_")
        if split_m[1]=="cogn":
            x.append(split_m[0])

    sifis=[]
    sifis_q=[]
    crap=[]
    skunk=[]
    for i in range(len(avg_cyc)):
        sifis.append( [avg_cyc[i][0], avg_cogn[i][0], max_cyc[i][0], max_cogn[i][0]])
        sifis_q.append( [avg_cyc[i][1], avg_cogn[i][1], max_cyc[i][1], max_cogn[i][1]])
        crap.append( [avg_cyc[i][2], avg_cogn[i][2], max_cyc[i][2], max_cogn[i][2]])
        skunk.append( [avg_cyc[i][3], avg_cogn[i][3], max_cyc[i][3], max_cogn[i][3]])
    print_plot(x,sifis,'./img/Static/'+image_name+'_sifis.png',"Sifis")
    print_plot(x,sifis_q,'./img/Static/'+image_name+'_sifis_quantized.png',"Sifis Quantized")
    print_plot(x,crap,'./img/Static/'+image_name+'_crap.png',"CRAP")
    print_plot(x,skunk,'./img/Static/'+image_name+'_skunk.png',"SkunkScore")
    return

static_analysis("./StaticAnalysis","static_analysis")