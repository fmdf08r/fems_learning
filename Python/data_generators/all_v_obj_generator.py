import pandas as pd
import sys

obj_path = "../../data/obj_pred/obj_pred_"
obj_ext = ".obj"

init_obj = pd.read_csv('../../data/obj_files/obj_info_0.csv',header=0)
velocities = pd.read_csv('../../data/point_by_point/testing_pred.csv',header=0)


#########

max_time = int( velocities['t'].max(axis=0) )
min_time = int ( velocities['t'].min(axis=0) )

sys.stdout.write(str(min_time) + "\n")
sys.stdout.write(str(max_time) + "\n")

delta_t = 0.3333

vertices_p = {}
faces = {}
for t in range(min_time, max_time + 1):
    sys.stdout.write("time: " + str(t) + "\n")
    sys.stdout.flush()
    vertices_c = {}
    data = pd.DataFrame()
    sys.stdout.write("saving dictionaries")
    if t == 0:
    	data = init_obj.loc[:, ['el','v1','v2','v3','v4','p1x','p1y','p1z','p2x','p2y','p2z','p3x','p3y','p3z','p4x','p4y','p4z'] ]
	for idx, row in data.iterrows():
	    faces[ int(row['el']) ] = "f " + str(int(row['v1'])) + " " + str( int(row['v2']) ) + " " + str( int(row['v3']) ) + " " + str( int(row['v4']) ) + "\n"
    	    vertices_c[ int(row['v1']) ] = [ float(row['p1x']), float(row['p1y']), float(row['p1z']) ]
	    vertices_c[ int(row['v2']) ] = [ float(row['p2x']), float(row['p2y']), float(row['p2z']) ]
	    vertices_c[ int(row['v3']) ] = [ float(row['p3x']), float(row['p3y']), float(row['p3z']) ]
	    vertices_c[ int(row['v4']) ] = [ float(row['p4x']), float(row['p4y']), float(row['p4z']) ]
    else:
	temp = velocities.loc[:, ['t','v','vx','vy','vz'] ] 
	data = temp.loc[ temp['t'] == t ]
	for idx, row in data.iterrows():
	    if  not vertices_p: 
	    	sys.stdout.write("dictionary is empty\n")
	    v = int( row['v'] )
	    vertices_p[ v ]
	    px = vertices_p[ v ][0] + delta_t * float( row['vx'] )
	    py = vertices_p[ v ][1] + delta_t * float( row['vy'] )
	    pz = vertices_p[ v ][2] + delta_t * float( row['vz'] )
	    vertices_c[v] = [px, py, pz]
	    #vertices_c[ int(row['v']) ] = [ vertices_p[ int(row['v']) ][0] + delta_t * float(row['vx']), vertices_p[ int(row['v']) ][1] + delta_t * float(row['vy']),  vertices_p[ int(row['v']) ][2] + delta_t * float(row['vz']) ] 
    sys.stdout.write("... completed\n")
    vertices_p = vertices_c
    sys.stdout.write("writing to file")
    sorted_v = sorted(vertices_c.keys())
    sorted_f = sorted(faces.keys())
    with open(obj_path + str(t) + obj_ext, 'wb') as obj_w:
	for k in sorted_v:
	    v = vertices_c[ k ]
	    output = "v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n"
	    obj_w.write( output  )
	for k in sorted_f:
	    obj_w.write( faces[k] )
        obj_w.close()
    sys.stdout.write("... complete\n")
