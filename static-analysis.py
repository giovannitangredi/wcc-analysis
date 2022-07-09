
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def get_ticks(Y_axis):
    vec=[y for ys in Y_axis for y in ys]
    ymin= min(vec)
    ymax= max(vec)
    #delta = (ymax-ymin)/200
    #res=[]
    #vec.sort()
    #for i in range(1,len(vec)):
        #if(vec[i]-vec[i-1]>delta) :
            #res.append(vec[i-1])
   #res.append(vec[len(vec)-1])
    npv=np.linspace(ymin,ymax,30)
    #res = npv[0::2]
    #for x in npv:
        #res.append(x)
    return npv

#avg_cyc[, avg_cogn, max_cyc, max_cogn,min_cyc, min_cogn
def print_bar_plot(x,vec,img_path,title): 
   
    V_axis = []
    X_axis = np.arange(len(x))
    Y_axis=[]
    for v in x:
        V_axis.append([v+'_AVG_CYC',v+'_MAX_CYC',v+'_MIN_CYC',v+'_AVG_COG',v+'_MAX_COG',v+'_MIN_COG'])
    min_y=float("inf")
    max_y=0
    for rows in vec:
        Y_axis.append([rows[0],rows[2],rows[4],rows[1],rows[3],rows[5]])
    for y in Y_axis:
        for value in y:
            min_y=min(min_y,value)
            max_y=max(max_y,value)
    plt.rcParams.update({'font.size': 18})
    figure(figsize=(36,30), dpi=80)
    for i in range(0,len(x)):
        bar=plt.barh(V_axis[i], Y_axis[i], 0.6, label = x[i])
        plt.bar_label(bar,padding=5)
    #    for j in range(0,len(Y_axis[i])):
    #        plt.text(V_axis[i][j], Y_axis[i][j]//2,str(round(Y_axis[i][j],2)), color='black', ha='center', fontweight='bold')
    #plt.yticks(rotation='vertical')
    plt.xticks(get_ticks(Y_axis),rotation=45)
    plt.xlim(min_y)
    plt.xlabel("projects",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
    plt.ylabel("Complexity",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.title(title)
    plt.legend()
    plt.savefig(img_path)
    plt.cla()
    return

def static_analysis(path_to_csvs,image_name):
    files = []
    avg_cyc= []
    max_cyc= []
    min_cyc= []
    avg_cogn= []
    max_cogn= []
    min_cogn= []
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
                if row[0] == 'MIN':
                     if file.split("_")[1] == "cyc.csv":
                        min_cyc.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                     else:
                        min_cogn.append([float(row[1]),float(row[2]),float(row[3]),float(row[4])])
                        
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
        sifis.append( [avg_cyc[i][0], avg_cogn[i][0], max_cyc[i][0], max_cogn[i][0],min_cyc[i][0], min_cogn[i][0]])
        sifis_q.append( [avg_cyc[i][1], avg_cogn[i][1], max_cyc[i][1], max_cogn[i][1],min_cyc[i][1], min_cogn[i][1]])
        crap.append( [avg_cyc[i][2], avg_cogn[i][2], max_cyc[i][2], max_cogn[i][2],min_cyc[i][2], min_cogn[i][2]])
        skunk.append( [avg_cyc[i][3], avg_cogn[i][3], max_cyc[i][3], max_cogn[i][3],min_cyc[i][3], min_cogn[i][3]])
    print_bar_plot(x,sifis,'./img/Static/'+image_name+'_wcc_plain.png',"WCC Plain")
    print_bar_plot(x,sifis_q,'./img/Static/'+image_name+'_wcc_quantized.png',"WCC Quantized")
    print_bar_plot(x,crap,'./img/Static/'+image_name+'_crap.png',"CRAP")
    print_bar_plot(x,skunk,'./img/Static/'+image_name+'_skunk.png',"SkunkScore")
    return

static_analysis("./StaticAnalysis","static_analysis")