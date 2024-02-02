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
_2d = False
_3d = True

## 2D
# add city nodes
if _2d==True:
    for id, city in functions.city_w.items():
        world_map_graph.add_node(id, name=city['name'], has_harbor=city['harbor'], can_harbor=city['can_harbor'])

    # add routes
    for edge in functions.tickets_w:
        city1, city2, weight, _type, color = edge
        world_map_graph.add_edge(city1, city2, weight=weight, _type=_type, color=functions.colors[color])
    # get pos from viz
    pos = nx.planar_layout(world_map_graph)
    # draw nodes
    nx.draw_networkx_nodes(world_map_graph, pos, node_size=200)
    # draw edges
    for edge in world_map_graph.edges(data=True): # split into a, b, data['x': 'y', ...]
        nx.draw_networkx_edges(world_map_graph, pos, edgelist=[(edge[0],edge[1])], edge_color=edge[2]['color'])

    nx.draw_networkx_labels(world_map_graph, pos)
    plt.show()


### 3D
# plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



# add cities
for id, city in functions.city_w.items():
    world_map_graph.add_node(id, name=city['name'], has_harbor=city['harbor'], can_harbor=city['can_harbor'])

# add routes
for edge in functions.tickets_w:
    city1, city2, weight, _type, color = edge
    world_map_graph.add_edge(city1, city2, weight=weight, _type=_type, color=functions.colors[color])

# get pos from viz
pos = nx.spring_layout(world_map_graph, dim=3, seed=70)

# rescale length to reflect weight
""" for edge in world_map_graph.edges(data=True):
    weight = edge[2]['weight']
    scale_factor = weight / 2  # Adjust the scaling factor as needed

    # Rescale node positions
    pos[edge[0]] = [pos[edge[0]][0] * scale_factor, pos[edge[0]][1] * scale_factor, pos[edge[0]][2]]
    pos[edge[1]] = [pos[edge[1]][0] * scale_factor, pos[edge[1]][1] * scale_factor, pos[edge[1]][2]]
 """

#nodes gotten from layout
for node, (x, y, z) in pos.items():
    ax.scatter(x, y, z, c='b', marker='x', label=node, sizes=[8])
    ax.text(x, y, z, node, fontsize=8, color='black')

# Draw edges
double_edges=set()
for edge in world_map_graph.edges(data=True):

    weight = edge[2]['weight']
    num_points = 200
    t = np.linspace(0, 1, num_points)

    p0 = np.array([pos[edge[0]][0], pos[edge[0]][1], pos[edge[0]][2]])
    p2 = np.array([pos[edge[1]][0], pos[edge[1]][1], pos[edge[1]][2]])
    p1 = (p0 + p2) / 2

    # if there exist two or more edges between two nodes
    if(edge[0],edge[1]) in double_edges or (edge[1],edge[0]) in double_edges:
        # Midpoint as control point with an offset in the x-direction
        offset_amount = np.random.uniform(-0.10,0.10,size=3)  # You can adjust this value
        p1 = (p0 + p2) / 2 + np.array(offset_amount)
    else:
        double_edges.add((edge[0],edge[1]))
        double_edges.add((edge[1],edge[0]))   

    # Define the Bezier curve for each coordinate
    x_curve = functions.bezier_curve(p0[0], p1[0], p2[0], t)
    y_curve = functions.bezier_curve(p0[1], p1[1], p2[1], t)
    z_curve = functions.bezier_curve(p0[2], p1[2], p2[2], t)
    curves = Line3DCollection([list(zip(x_curve, y_curve, z_curve))], colors=edge[2]['color'], alpha=0.5)    
    ax.add_collection3d(curves)

background_color = 'white'
ax.xaxis.set_pane_color(mpl.colors.to_rgba(background_color))
ax.yaxis.set_pane_color(mpl.colors.to_rgba(background_color))
ax.zaxis.set_pane_color(mpl.colors.to_rgba(background_color))

plt.show()

########################################################################
##########################    GREAT LAKES   ############################
########################################################################   