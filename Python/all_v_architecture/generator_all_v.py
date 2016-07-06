import sys
import pandas as pd
from collections import defaultdict

obj_path = "../../data/obj_files/obj_info_"
data_path = "../../data/all_v/"
ext = ".csv"

timesteps = 18000

with open(data_path + "data_set.csv",'wb') as d:
    with open(data_path + "labels_set.csv", "wb") as l:
        for t in range(timesteps -1):
            sys.stdout.write("Time = " + str(t) + "\n")
            
            sys.stdout.write("- Generating Dictionaries: ")
            
	    t_now = defaultdict(str)
            df_now = pd.read_csv(obj_path + str(t) + ext,header=0) 
            for idx, row in df_now.iterrows():
                t_now[ int(row['v1']) ] = str(row['p1x']) + "," + str(row['p1y']) + "," + str(row['p1z']) + "," + str(row['v1x']) + "," + str(row['v1y']) + "," + str(row['v1z']) + "," + str(row['f1x']) + "," + str(row['f1y']) + "," + str(row['f1z'])
                t_now[ int(row['v2']) ] = str(row['p2x']) + "," + str(row['p2y']) + "," + str(row['p2z']) + "," + str(row['v2x']) + "," + str(row['v2y']) + "," + str(row['v2z']) + "," + str(row['f2x']) + "," + str(row['f2y']) + "," + str(row['f2z'])  
                t_now[ int(row['v3']) ] = str(row['p3x']) + "," + str(row['p3y']) + "," + str(row['p3z']) + "," + str(row['v3x']) + "," + str(row['v3y']) + "," + str(row['v3z']) + "," + str(row['f3x']) + "," + str(row['f3y']) + "," + str(row['f3z']) 
                t_now[ int(row['v4']) ] = str(row['p4x']) + "," + str(row['p4y']) + "," + str(row['p4z']) + "," + str(row['v4x']) + "," + str(row['v4y']) + "," + str(row['v4z']) + "," + str(row['f4x']) + "," + str(row['f4y']) + "," + str(row['f4z']) 
	    
            t_next = defaultdict(list)
            df_next = pd.read_csv(obj_path + str(t+1) + ext,header=0)
            for idx, row in df_next.iterrows():
                t_next[ int(row['v1']) ] = str(row['v1x']) + "," + str(row['v1y']) + "," + str(row['v1z'])
                t_next[ int(row['v2']) ] = str(row['v2x']) + "," + str(row['v2y']) + "," + str(row['v2z'])
                t_next[ int(row['v3']) ] = str(row['v3x']) + "," + str(row['v3y']) + "," + str(row['v3z'])
                t_next[ int(row['v4']) ] = str(row['v4x']) + "," + str(row['v4y']) + "," + str(row['v4z'])
            sys.stdout.write("completed\n")
            sys.stdout.write("- Saving DATA")
	    sorted_v = sorted( t_now.keys() )
            s = str(t) + ","
            for i in range(len(sorted_v)): 
                s = s + t_now[ sorted_v[i] ]
                if i < len(sorted_v) - 1:
                    s = s + ","
            d.write( s + "\n")
            sys.stdout.write("-> completed\n")
	    
            sys.stdout.write("- Saving LABELS")
            sorted_v = sorted( t_next.keys() )
            s = str(t+1) + ","
            for i in range(len(sorted_v)): 
                s = s + t_next[ sorted_v[i] ]
                if i < len(sorted_v) - 1:
                    s = s + ","
            l.write( s + "\n" )
            sys.stdout.write("-> completed\n")
        l.close()
    d.close()
