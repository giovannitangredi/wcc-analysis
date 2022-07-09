import os
import csv
from importlib_metadata import version
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
    plt.rcParams.update({'font.size': 18})
    plt.rcParams["figure.autolayout"] = True
    figure(figsize=(22,16), dpi=80)
    #bar1=plt.bar(versions, total, 0.4, label="Remaining number of files")
    #bar2=plt.bar(versions, complex, 0.4,color="r", label="number of complex files")
    for i in range(0,len(versions)):
        #plt.text(i, complex[i]//2,str(complex[i]), color='black', ha='center', fontweight='bold')
        plt.text( (total[i]-complex[i])//2 +complex[i],i,str(total[i]-complex[i]), color='snow', va='center',ha='center',fontweight='bold')
    bar1=plt.barh(versions, total, 0.4, label="Remaining number of files")
    bar2=plt.barh(versions, complex, 0.4,color="r", label="Number of complex files")
    plt.bar_label(bar1,padding=5,fontweight='bold')
    plt.bar_label(bar2,label_type='center',color="snow",fontweight='bold')
    yt=versions.copy()
    yt.append("")
    plt.yticks(yt)
    plt.ylabel("versions",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.xlabel("number of complex files",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
    plt.title("Complex files")
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1,0]
    plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc='upper right',prop={'size': 20})
    plt.savefig(img_path)
    plt.cla()
    return

def plot_complex_percentage(versions,complex,total,img_path):
    plt.rcParams.update({'font.size': 18})
    plt.rcParams["figure.autolayout"] = True
    figure(figsize=(22,16), dpi=80)
    ratios = np.divide(complex,total)
    ratios= np.multiply(ratios,100.0)
    plt.barh(versions, np.full(len(versions),100), 0.3, label="Remaining number of files")
    bar=plt.barh(versions, ratios, 0.3,color="r", label="Percentage of complex files")
    for i in range(0,len(versions)):
        plt.text(ratios[i]+((100.0-ratios[i])//2), i,str(round(100.0-ratios[i],2))+"%", color='snow',va='center', ha='center',fontweight='bold')
    plt.bar_label(bar,label_type='center',color="snow",fmt="%.2f %%",fontweight='bold')
    yt=versions.copy()
    yt.append("")
    plt.yticks(yt)
    plt.ylabel("versions",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.xlabel("percentage of complex files",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
    plt.title("Complex files Percentage")
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1,0]
    plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc='upper right',prop={'size': 20})
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
    plot_complex_percentage(versions,n_complex,n_files,'./img/Time/'+image_name+'_complex_files_percentage.png')
    return

time_analysis("./TimeAnalysis/rust-analyzer","rust-analyzer")
time_analysis("./TimeAnalysis/seahorse","seahorse")
    