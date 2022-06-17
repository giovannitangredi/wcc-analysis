import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def print_plot(versions,vec,img_path):
    sifis=[]
    sifis_q=[]
    crap=[]
    skunk=[]
    for rows in vec:
        sifis.append(rows[0])
        sifis_q.append(rows[1])
        crap.append(rows[2])
        skunk.append(rows[3])
    plt.rcParams.update({'font.size': 12})
    figure, axis = plt.subplots(2, 2)
    figure.set_size_inches(24, 20)
    axis[0, 0].plot(versions, sifis)
    axis[0, 0].scatter(versions, sifis,color="r")
    axis[0, 0].set_title("WCC Plain")
    axis[0, 0].set_xlabel('versions')
    axis[0, 1].plot(versions, sifis_q)
    axis[0, 1].scatter(versions, sifis_q,color="r")
    axis[0, 1].set_title("WCC Quantized")
    axis[0, 1].set_xlabel('versions')
    axis[1, 0].plot(versions, crap)
    axis[1, 0].scatter(versions, crap,color="r")
    axis[1, 0].set_title("CRAP")
    axis[1, 0].set_xlabel('versions')
    axis[1, 1].plot(versions, skunk)
    axis[1, 1].scatter(versions, skunk,color="r")
    axis[1, 1].set_title("SkunkScore")
    axis[1, 1].set_xlabel('versions')
    plt.savefig(img_path)
    plt.cla()
    return

def plot_complex(versions,complex,total,img_path):
    plt.rcParams.update({'font.size': 12})
    plt.rcParams["figure.autolayout"] = True
    figure(figsize=(20,11), dpi=80)
    ratios = np.divide(complex,total)
    ratios= np.multiply(ratios,100.0)
    plt.bar(versions, np.full(len(versions),100), 0.3, label="Total number of files")
    plt.bar(versions, ratios, 0.3,color="r", label="percentage of complex files")
    plt.xlabel("versions")
    plt.ylabel("Number of complex files")
    plt.title("Complex files")
    plt.legend()
    plt.savefig(img_path)
    plt.cla()
    return

def time_analysis(path_to_csvs, image_name) :
    files = []
    avg= []
    max= []
    n_complex = []
    n_files = []
    for file in os.listdir(path_to_csvs):
        if file.endswith(".csv"):
            files.append(file)

    files.sort()
    for file in files:
        cf =0
        tf =0
        with open(path_to_csvs+"/"+file) as data:
            csvreader = csv.reader(data)
            header = next(csvreader)
            for row in csvreader:
                if row[6] == 'true':
                    cf+=1
                    tf+=1
                if row[0] != 'AVG' and row[0] != 'MAX' and row[6]=='false':
                    tf+=1
                if row[0] == 'AVG':
                    avg.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                if row[0] == 'MAX':
                    max.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                    break
        n_complex.append(cf)
        n_files.append(tf)
    versions=[]

    for f in files:
        no_ext_f = f[:len(f) - 4]
        versions.append("-".join(no_ext_f.split("-")[1:]))

    print_plot(versions,avg,'./img/Time/'+image_name+'_avg.png')
    print_plot(versions,max,'./img/Time/'+image_name+'_max.png')
    plot_complex(versions,n_complex,n_files,'./img/Time/'+image_name+'_complex_files.png')
    return

time_analysis("./TimeAnalysis/rust-analyzer","rust-analyzer")
time_analysis("./TimeAnalysis/seahorse","seahorse")
    