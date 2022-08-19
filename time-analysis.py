import os
import csv
import json
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
        plt.text(i, (total[i]-complex[i])//2 +complex[i],str(total[i]-complex[i]), color='snow', va='center',ha='center',fontweight='bold')
    bar1=plt.bar(versions, total, 0.4, label="Remaining number of files")
    bar2=plt.bar(versions, complex, 0.4,color="r", label="Number of complex files")
    plt.bar_label(bar1,padding=5,fontweight='bold')
    plt.bar_label(bar2,label_type='center',color="snow",fontweight='bold')
    yt=plt.yticks()[0].tolist()
    step = yt[1]-yt[0]
    #yt.append(max(yt)+step)
    plt.yticks(yt)
    plt.ylabel("number of complex files",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.xlabel("versions",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
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
    plt.bar(versions, np.full(len(versions),100), 0.5, label="Remaining number of files")
    bar=plt.bar(versions, ratios, 0.5,color="r", label="Percentage of complex files")
    for i in range(0,len(versions)):
        plt.text(i,ratios[i]+((100.0-ratios[i])//2),str(round(100.0-ratios[i],2))+"%", color='snow',va='center', ha='center',fontweight='bold')
    plt.bar_label(bar,label_type='center',color="snow",fmt="%.2f%%",fontweight='bold')
    yt=plt.yticks()[0].tolist()
    step = yt[1]-yt[0]
    #yt.append(max(yt)+step)
    plt.yticks(yt)
    plt.ylabel("percentage of complex files",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.xlabel("versions",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
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


 ### FUNCTIONS

def check_not_cum(file_name):
    return file_name != "AVG" and file_name != "MAX" and file_name != "MIN" and file_name != "PROJECT"


def plot_complex_functions(image_path,map,map_complex):
    plt.rcParams.update({'font.size': 18})
    plt.rcParams["figure.autolayout"] = True
    figure(figsize=(22,16), dpi=80)
    x=[]
    total=[]
    complex=[]
    for key,roots in map.items():
        no_ext_f = key[:len(key) - 4]
        x.append("-".join(no_ext_f.split("-")[1:]))
        complex.append(map_complex[key])
        vt=0
        for r in roots:
            vt += len(r["functions"])
        total.append(vt)
    for i in range(0,len(x)):
        plt.text(i, (total[i]-complex[i])//2 +complex[i],str(total[i]-complex[i]), color='snow', va='center',ha='center',fontweight='bold')
        if complex[i]>2:
            plt.text(i, (complex[i])//2,str(complex[i]), color='snow', va='center',ha='center',fontweight='bold')
        else:
            plt.text(i, (complex[i])+1,str(complex[i]), color='snow', va='center',ha='center',fontweight='bold')
    bar1=plt.bar(x, total, 0.4, label="Remaining number of function")
    bar2=plt.bar(x, complex, 0.4,color="r", label="Number of complex function")
    plt.bar_label(bar1,padding=5,fontweight='bold')
    #plt.bar_label(bar2,padding=10,label_type='center',color="snow",fontweight='bold')
    yt=plt.yticks()[0].tolist()
    step = yt[1]-yt[0]
    yt.append(max(yt)+step)
    plt.yticks(yt)
    plt.ylabel("versions",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.xlabel("number of complex functions",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
    plt.title("Complex function")
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1,0]
    plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc='upper right',prop={'size': 20})
    plt.savefig(image_path+".png")
    plt.cla()
    # PErcentage
    ratios = np.divide(complex,total)
    ratios= np.multiply(ratios,100.0)
    for i in range(0,len(x)):
        plt.text(i, (100.0-ratios[i])//2 +ratios[i],str(round(100.0-ratios[i],2))+"%", color='snow', va='center',ha='center',fontweight='bold')
        if ratios[i]>2-0:
            plt.text(i, (ratios[i])//2,str((round(ratios[i],2)))+"%", color='snow', va='center',ha='center',fontweight='bold')
        else:
            plt.text(i, (ratios[i])+1.0,str((round(ratios[i],2)))+"%", color='snow', va='center',ha='center',fontweight='bold')
    bar1=plt.bar(x, np.full(len(x),100), 0.5, label="Remaining percentage of function")
    bar2=plt.bar(x, ratios, 0.5,color="r", label="Percentage of complex function")
    #plt.bar_label(bar1,padding=5,fontweight='bold')
    #plt.bar_label(bar2,label_type='center',fmt="%.2f %%",color="snow",fontweight='bold')
    yt=plt.yticks()[0]
    #yt.append()
    plt.yticks(yt)
    plt.ylabel("versions",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.xlabel("number of complex functions",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
    plt.title("Complex function Percentage")
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1,0]
    plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc='upper right',prop={'size': 20})
    plt.savefig(image_path+"_percentage.png")
    plt.cla()
    return

def print_mcf_per_comp(image_name,map,metric):
    map_mcf = dict()
    map_x = dict()
    mcf = ("",0.0)
    for key,roots in map.items():
        mcf = ("",0.0)
        for r in roots:
            for f in r["functions"]:
                f_name=f["function_name"].split(" ")[0]
                comp = f["metrics"][metric]
                if comp >= mcf[1]:
                    mcf = (f_name,comp) 
        if mcf[0] in map_mcf:
            map_mcf[mcf[0]].append(mcf[1])
        else:
            map_mcf[mcf[0]]=[]
            map_mcf[mcf[0]].append(mcf[1])
        if mcf[0] in map_x:
            map_x[mcf[0]].append(key)
        else:
            map_x[mcf[0]]=[]
            map_x[mcf[0]].append(key)
    plt.rcParams.update({'font.size': 18})
    plt.rcParams["figure.autolayout"] = True
    for keyf,value in map_mcf.items():
        ##wcc plain for noe for testing
        x=map_x[keyf]
        y = value
        x_axis= ["-".join(k[0:len(k)-5].split("-")[1:]) for k in x ]
        plt.plot(x_axis,y,label=keyf)
        plt.scatter(x_axis,y)
    plt.xticks(rotation=45)
    plt.ylabel("most complex function",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.xlabel("versions",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
    plt.title("Most complex function - "+metric)
    plt.legend()
    plt.savefig(image_name+"_"+metric+".png")
    plt.cla()
    return

def print_mcf_per_repo(image_name,map):
    print_mcf_per_comp(image_name,map,"sifis_plain")
    print_mcf_per_comp(image_name,map,"sifis_quantized")
    print_mcf_per_comp(image_name,map,"crap")
    print_mcf_per_comp(image_name,map,"skunk")
    return

def print_time_msf_bar(image_name,map,complexity):
    all_x =[]
    x_ticks=[]
    l=0
    for key,roots in map.items():
        functions = [f for root in roots  for f in root["functions"]]
        no_ext_k = key[0:len(key)-5]
        version = "-".join(no_ext_k.split("-")[1:])
        functions.sort(key=lambda x: x["metrics"][complexity], reverse=True)
        functions=functions[0:3]
        x = [x["function_name"] for x in functions]
        y = [x["metrics"][complexity] for x in functions]
        all_x.append(x)
        ticks= np.arange(len(x))
        ticks = [t + l for t in ticks]
        l= l+len(x)
        plt.rcParams.update({'font.size': 16})
        plt.rcParams["figure.autolayout"] = True
        bar = plt.bar(ticks,y,0.6,label=version)
        plt.bar_label(bar,padding=5,fontweight='bold',fmt="%.2f")
    plt.bar(["","","","",""],[0,0,0,0,0])
    all_x.append(["","",""])
    all_x = [el for x in all_x for el in x]
    x_ticks = np.arange(len(all_x))
    plt.xticks(x_ticks,all_x,rotation=90)
    plt.ylabel("complexity",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.xlabel("functions per version",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
    plt.title("Most 3 complex function per version")
    plt.legend()
    plt.savefig(image_name+"_"+complexity+".png")
    plt.cla()
    return
def print_time_msf(image_name,map):
    print_time_msf_bar("./img/Time/functions/"+image_name+"_fpv",map,"sifis_plain")
    print_time_msf_bar("./img/Time/functions/"+image_name+"_fpv",map,"sifis_quantized")
    print_time_msf_bar("./img/Time/functions/"+image_name+"_fpv",map,"crap")
    print_time_msf_bar("./img/Time/functions/"+image_name+"_fpv",map,"skunk")
    return

def time_analysis_functions(path_to_jsons, image_name):
    versions=[]
    map = dict()
    map_complex = dict()
    for file in os.listdir(path_to_jsons):
        if file.endswith(".json"):
            versions.append(file)
    versions.sort()
    for v in versions:
        roots=[]
        f= open(path_to_jsons+"/"+v)
        data = json.load(f)
        map_complex[v]=data["number_of_complex_functions"]
        for m in data["files"]:
            if check_not_cum(m["file_name"]):
                roots.append(m)
        map[v]= roots.copy()
    plot_complex_functions("./img/Time/functions/"+image_name+"_complex",map,map_complex)
    print_mcf_per_repo("./img/Time/functions/"+image_name+"_most_complex_function",map)
    print_time_msf(image_name,map)

time_analysis("./TimeAnalysis/rust-analyzer","rust-analyzer")
time_analysis("./TimeAnalysis/seahorse","seahorse")
time_analysis_functions("./TimeAnalysis/rust-analyzer","rust-analyzer")
time_analysis_functions("./TimeAnalysis/seahorse","seahorse")
    