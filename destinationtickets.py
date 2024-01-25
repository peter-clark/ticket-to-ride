import os
import csv
import numpy
import heapq
import functions

## get data ##
wm = []
wm_f = os.getcwd()+"/data/WorldMap.csv"
with open(wm_f) as f:
    reader = csv.reader(f)
    for row in reader:
        wm.append(row)
    f.close()

gl = []
gl_f = os.getcwd()+"/data/GreatLakes.csv"
with open(gl_f) as f:
    reader = csv.reader(f)
    for row in reader:
        gl.append(row)
    f.close()

functions.nothing()


########################################################################
############################    WORLD MAP   ############################
########################################################################   

## init ##
worldmap = functions.initialize_world()
ticket_list = functions.initialize_world_tickets()

## show ##
""" worldmap.display_graph() """
""" ticket_list.print_tickets() """

## route mapping ##
start='NYC'
end='JAK'
max_len = 16
max_ships = max_len
max_trains = max_len

map_routes = True
if map_routes:
    sorted_routes = worldmap.get_sorted_paths(start, end, max_len, max_ships, max_trains)
    print(f"Shortest Route:")
    functions.print_sorted_paths(sorted_routes[:1])
    print(f"All Routes:")
    functions.print_sorted_paths(sorted_routes)



########################################################################
##########################    GREAT LAKES   ############################
########################################################################   