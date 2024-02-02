import os
import csv
import heapq
import networkx as nx
import functions
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

_worldmap = False

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

map_routes = False
if map_routes:
    sorted_routes = worldmap.get_sorted_paths(start, end, max_len, max_ships, max_trains)
    print(f"Shortest Route:")
    functions.print_sorted_paths(sorted_routes[:1])
    print(f"All Routes:")
    functions.print_sorted_paths(sorted_routes)


## Graph building and viz
world_map_graph = nx.MultiGraph()
world_map_graph.clear()
gl_map_graph = nx.MultiGraph()
gl_map_graph.clear()

_2d = True
_3d = False

## 2D
# add city nodes
if _2d==True:
    functions.graph2D(gl_map_graph, functions.city_gl,  functions.connections_gl, functions.fixed_gl)
    

if _3d:
    functions.graph3D(gl_map_graph, functions.city_gl, functions.connections_gl)

########################################################################
##########################    GREAT LAKES   ############################
########################################################################   