import csv 
import sys
from collections import defaultdict

reader_path = "../../data/obj_files/obj_info_"
reader_extension = ".csv"

writer_path = "../../data/obj_files/timestep_"
writer_extension = ".obj"

num_time_steps = 600 

sys.stdout.write("Parsing obj files: ")
for i in range(num_time_steps):
    sys.stdout.write(str(i) + " - ")
    sys.stdout.flush()
    obj_reader = reader_path + str(i) + reader_extension
   
    vertices = defaultdict(list)
    elements = defaultdict(list)
    with open(obj_reader, 'r') as r:
        reader = csv.DictReader(r)
        for row in reader:
            elements[ int(row['el']) ].append( float(row['v1']) )
            elements[ int(row['el']) ].append( float(row['v2']) )
            elements[ int(row['el']) ].append( float(row['v3']) )
            elements[ int(row['el']) ].append( float(row['v4']) )

            vertices[ int(row['v1']) ].append( float(row['p1x']) )
            vertices[ int(row['v1']) ].append( float(row['p1y']) )
            vertices[ int(row['v1']) ].append( float(row['p1z']) )

            vertices[ int(row['v2']) ].append( float(row['p2x']) )
            vertices[ int(row['v2']) ].append( float(row['p2y']) )
            vertices[ int(row['v2']) ].append( float(row['p2z']) )

            vertices[ int(row['v3']) ].append( float(row['p3x']) )
            vertices[ int(row['v3']) ].append( float(row['p3y']) )
            vertices[ int(row['v3']) ].append( float(row['p3z']) )

            vertices[ int(row['v4']) ].append( float(row['p4x']) )
            vertices[ int(row['v4']) ].append( float(row['p4y']) )
            vertices[ int(row['v4']) ].append( float(row['p4z']) )
        r.close()
    sorted_v = sorted( vertices.keys() ) 
    sorted_el = sorted( elements.keys() )
    obj_writer = writer_path + str(i) + writer_extension
    with open(obj_writer, 'wb') as w:
        for k in sorted_v:
	    v = vertices[ k ]
            w.write("v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n")
	for k in sorted_el:
	    #sys.stdout.write( str(k) + " - " )
	    #sys.stdout.flush()
            v = elements[ k ]  
	    w.write("f " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + " " + str(v[3]) + "\n")
        w.close()
sys.stdout.write(" complete\n")
