import sys
import pandas as pd
from collections import defaultdict

filePath = "../../data/obj_files/obj_info_"
ext = ".csv"

faces = defaultdict(str)
faces_saved = False
timesteps = 600
names=[]
header_v = "t,v,px,py,pz,vx,vy,vz,fx,fy,fz\n"
header_l = "t,v,vx,vy,vz\n"

with open('../../data/point_by_point/data_set.csv','wb') as d:
    d.write(header_v)
    for t in range(timesteps - 1):
        sys.stdout.write("time = " + str(t) + "\n")
        sys.stdout.flush()
        vertices_p = defaultdict(str)    
        vpName = filePath + str(t) + ext
        sys.stdout.write("saving current vertices:")
        vp_df = pd.read_csv(vpName, header=0)
        for idx, row in vp_df.iterrows():
            if not faces_saved: 
                faces[ int(row['el']) ] = "f " + str(int(row['v1'])) + " " + str(int(row['v2'])) + " " + str(int(row['v3'])) + " " + str(int(row['v4'])) + "\n"
            vertices_p[ int(row['v1']) ] = str(t) + "," + str(int(row['v1'])) + ","  + str(row['p1x']) + "," + str(row['p1y']) + "," + str(row['p1z']) + "," + str(row['v1x']) + "," + str(row['v1y']) + "," + str(row['v1z']) + "," + str(row['f1x']) + "," + str(row['f1y']) + "," + str(row['f1z']) + "\n"
            vertices_p[ int(row['v2']) ] = str(t) + "," + str(int(row['v2'])) + "," + str(row['p2x']) + "," + str(row['p2y']) + "," + str(row['p2z']) + "," + str(row['v2x']) + "," + str(row['v2y']) + "," + str(row['v2z']) + "," + str(row['f2x']) + "," + str(row['f2y']) + "," + str(row['f2z']) + "\n"  
            vertices_p[ int(row['v3']) ] = str(t) + "," + str(int(row['v3'])) + "," + str(row['p3x']) + "," + str(row['p3y']) + "," + str(row['p3z']) + "," + str(row['v3x']) + "," + str(row['v3y']) + "," + str(row['v3z']) + "," + str(row['f3x']) + "," + str(row['f3y']) + "," + str(row['f3z']) + "\n"  
            vertices_p[ int(row['v4']) ] = str(t) + "," + str(int(row['v4'])) + "," + str(row['p4x']) + "," + str(row['p4y']) + "," + str(row['p4z']) + "," + str(row['v4x']) + "," + str(row['v4y']) + "," + str(row['v4z']) + "," + str(row['f4x']) + "," + str(row['f4y']) + "," + str(row['f4z']) + "\n" 
        faces_saved = True
        sys.stdout.write("completed\n")
        sys.stdout.write('writing current vertices: ')
	sorted_v = sorted( vertices_p.keys() )
        for k in sorted_v:
            d.write( vertices_p[ k ] )
        sys.stdout.write("completed\n")
    d.close()        

sys.stdout.write("writing faces: ")
with open('../../data/point_by_point/faces.txt','wb') as f:
    sorted_f = sorted( faces.keys() )
    for k in sorted_f:
        f.write( faces[ k ] )
    f.close()
sys.stdout.write(" completed\n")

with open('../../data/point_by_point/labels_set.csv','wb') as l:
    l.write(header_l)
    for t in range(timesteps - 1):
        sys.stdout.write("time =  " + str(t) + "\n")
	sys.stdout.write("saving next vertices:")
        sys.stdout.flush()
  	vertices_n = defaultdict(str)
        vnName = filePath + str(t + 1) + ext
        vn_df = pd.read_csv(vnName,header=0)
        for idx, row in vn_df.iterrows():
            vertices_n[ int(row['v1']) ] = str(t + 1) + "," + str(int(row['v1'])) + "," + str(row['v1x']) + "," + str(row['v1y']) + "," + str(row['v1z']) + "\n"
            vertices_n[ int(row['v2']) ] = str(t + 1) + "," + str(int(row['v2'])) + "," + str(row['v2x']) + "," + str(row['v2y']) + "," + str(row['v2z']) + "\n"  
            vertices_n[ int(row['v3']) ] = str(t + 1) + "," + str(int(row['v3'])) + "," + str(row['v3x']) + "," + str(row['v3y']) + "," + str(row['v3z']) + "\n"  
            vertices_n[ int(row['v4']) ] = str(t + 1) + "," + str(int(row['v4'])) + "," + str(row['v4x']) + "," + str(row['v4y']) + "," + str(row['v4z']) + "\n"
        sys.stdout.write("completed\n")
        sys.stdout.write("writing next vertices: ")
	sorted_v = sorted( vertices_n.keys() )
        for k in sorted_v:
            l.write( vertices_n[k] )
        sys.stdout.write("completed\n")
    l.close()
