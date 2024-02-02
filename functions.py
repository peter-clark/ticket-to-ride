# Helper functions for ticket-to-ride optimizer #
# 
import numpy as np
import networkx as nx
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#
## define classes ##------------------------------------------------------------------------------------
class WeightedGraph:
    def __init__(self):
        self.graph={}

    def add_edge(self, node1, node2, weight, type, color):

        # make nodes if not there
        if node1 not in self.graph:
            self.graph[node1] = {}
        if node2 not in self.graph:
            self.graph[node2] = {}

        ## add weight to edge, add edge if none
        if node2 not in self.graph[node1]:
            self.graph[node1][node2] = []
        self.graph[node1][node2].append({'weight':weight, 'type':type, 'color':color})

        if node1 not in self.graph[node2]:
            self.graph[node2][node1] = []
        self.graph[node2][node1].append({'weight':weight, 'type':type, 'color':color})

    def display_graph(self):
        for node in self.graph:
            print(f"--")
            for neighbor in self.graph[node]:
                for nghbr in self.graph[node][neighbor]:
                    p = nghbr['weight']
                    c = nghbr['color']
                    if c=='any':
                        c='a'
                    t = '==' if nghbr['type']==1 else '~~'
                    print(f"{node}: (t) {p}{c} {neighbor}")
    
    def all_paths(self, start, end, max_len=16):
        all_paths=[]
        
        # recurse ;)
        def dfs(current_node, path, visited, plen):  # depth first
            visited.add(current_node)

            for neighbor, edges in self.graph[current_node].items():
                for edge in edges:
                    weight = edge['weight']
                    if neighbor == end:
                        if plen + weight <= max_len:
                            # Append the edge to the path
                            path_with_edge = path + [(current_node, neighbor, weight, edge['type'], edge['color'])]
                            all_paths.append({'path': path_with_edge, 'type': edge['type'], 'color': edge['color']})
                    elif neighbor not in visited and plen + weight <= max_len:
                        # Append the edge to the path
                        path_with_edge = path + [(current_node, neighbor, weight, edge['type'], edge['color'])]
                        dfs(neighbor, path_with_edge, visited.copy(), plen + weight)

            visited.remove(current_node)

        dfs(start, [], set(), 0)

        return all_paths
    
    def get_shortest_path(self, start, end):
        paths=[]
        l = 1
        while paths==[]:
            paths = self.all_paths(start, end, max_len=l)
            l += 1
        return paths


    def get_sorted_paths(self, start, end, max_len, max_ships=35, max_trains=33):
        paths = self.all_paths(start, end, max_len)
        sorted_paths = sorted(paths, key=lambda x: sum(weight for _, _, weight, _, _ in x['path']))
        return sorted_paths


def print_sorted_paths(sorted_paths):
    printed_paths=set()
    for path in sorted_paths:
        path_info = path['path']
    
        # Make new tuple disregarding color and type for no duplicate printing
        path_tuple = tuple((node, neighbor, weight) for node, neighbor, weight, _, _ in path_info)
        
        if path_tuple not in printed_paths:
            printed_paths.add(path_tuple)

            # Calculate weights
            total_weight = sum(weight for _, _, weight, _, _ in path_info)
            ship_weight = sum(weight for _, _, weight, _type, _ in path_info if _type==2)
            train_weight = sum(weight for _, _, weight, _type, _ in path_info if _type==1)
            # Formatting
            if ship_weight<10:
                formatted_path = f"[{total_weight}] (~)0{ship_weight}/{train_weight}(=) >> "
                if train_weight<10:
                    formatted_path = f"[{total_weight}] (~)0{ship_weight}/0{train_weight}(=) >> "
            elif train_weight<10:
                formatted_path = f"[{total_weight}] (~){ship_weight}/0{train_weight}(=) >> "
                if ship_weight<10:
                    formatted_path = f"[{total_weight}] (~)0{ship_weight}/0{train_weight}(=) >> "
            else:
                formatted_path = f"[{total_weight}] (~){ship_weight}/{train_weight}(=) >> "

            for node, _, weight, type, _ in path_info:
                t = f'~~{weight}~~' if type==2 else f'=={weight}=='
                formatted_path += f"{node} {t} "

            formatted_path += path_info[-1][1] # add destination city name
            print(formatted_path)

class DestinationTicket:
    def __init__(self, node1, node2, value):
        self.ticket = [node1, node2, value]

class DestinationTickets:
    def __init__(self):
        self.tickets = {}

    def add_ticket(self, t):
        # make tuple ID
        key = (t.ticket[0], t.ticket[1]) # start, end
        if key not in self.tickets:
            self.tickets[key] = t.ticket[2] # value
    
    def print_tickets(self):
        for (a,b), value in self.tickets.items():
            print(f"[0{value}] {a} <-> {b}") if value<10 else print(f"[{value}] {a} <-> {b}")


## dictionary definitions ##
type = {1:'land', 2:'sea'}

colors = {# some changed for visibility
    'g':'green', 'p':'mediumvioletred', # heliotrope really
    'w':'indigo', 'r':'red', 'y':'yellow',
    'b':'black', 'any':'sienna', 'db':"darkslategray"
}

city_w = {
    'AAO': {'name': 'Antarctic Ocean', 'harbor': False, 'can_harbor': False},
    'ALQ': {'name': 'Al-Qahira', 'harbor': False, 'can_harbor': True},
    'ANC': {'name': 'Anchorage', 'harbor': False, 'can_harbor': True},
    'ATH': {'name': 'Athina', 'harbor': False, 'can_harbor': True},
    'BEI': {'name': 'Beijing', 'harbor': False, 'can_harbor': False},
    'BKK': {'name': 'Bangkok', 'harbor': False, 'can_harbor': True},
    'BUE': {'name': 'Buenos Aires', 'harbor': False, 'can_harbor': True},
    'CAR': {'name': 'Caracas', 'harbor': False, 'can_harbor': True},
    'CAS': {'name': 'Casablanca', 'harbor': False, 'can_harbor': True},
    'CMB': {'name': 'Cambridge Bay', 'harbor': False, 'can_harbor': True},
    'CPT': {'name': 'Cape Town', 'harbor': False, 'can_harbor': True},
    'CHR': {'name': 'Christchurch', 'harbor': False, 'can_harbor': True},
    'DES': {'name': 'Dar Es Salaam', 'harbor': False, 'can_harbor': True},
    'DJI': {'name': 'Djibouti', 'harbor': False, 'can_harbor': False},
    'EDI': {'name': 'Edinburgh', 'harbor': False, 'can_harbor': True},
    'HAM': {'name': 'Hamburg', 'harbor': False, 'can_harbor': True},
    'HKG': {'name': 'Hong Kong', 'harbor': False, 'can_harbor': True},
    'HON': {'name': 'Honolulu', 'harbor': False, 'can_harbor': True},
    'JAK': {'name': 'Jakarta', 'harbor': False, 'can_harbor': True},
    'LAH': {'name': 'Lahore', 'harbor': False, 'can_harbor': False},
    'LAG': {'name': 'Lagos', 'harbor': False, 'can_harbor': True},
    'LIM': {'name': 'Lima', 'harbor': False, 'can_harbor': True},
    'LOS': {'name': 'Los Angeles', 'harbor': False, 'can_harbor': True},
    'LUA': {'name': 'Luanda', 'harbor': False, 'can_harbor': True},
    'MAN': {'name': 'Manila', 'harbor': False, 'can_harbor': True},
    'MAR': {'name': 'Marseille', 'harbor': False, 'can_harbor': True},
    'MEX': {'name': 'Mexico', 'harbor': False, 'can_harbor': True},
    'MIA': {'name': 'Miami', 'harbor': False, 'can_harbor': True},
    'MOS': {'name': 'Moskva', 'harbor': False, 'can_harbor': False},
    'MUM': {'name': 'Mumbai', 'harbor': False, 'can_harbor': True},
    'NOV': {'name': 'Novosibirsk', 'harbor': False, 'can_harbor': True},
    'NYC': {'name': 'New York', 'harbor': False, 'can_harbor': True},
    'PER': {'name': 'Perth', 'harbor': False, 'can_harbor': True},
    'PET': {'name': 'Petropavlovsk', 'harbor': False, 'can_harbor': True},
    'PTM': {'name': 'Port Moresby', 'harbor': False, 'can_harbor': True},
    'REY': {'name': 'Reykjavik', 'harbor': False, 'can_harbor': True},
    'RIO': {'name': 'Rio De Janeiro', 'harbor': False, 'can_harbor': True},
    'SYD': {'name': 'Sydney', 'harbor': False, 'can_harbor': True},
    'TOA': {'name': 'Toamasina', 'harbor': False, 'can_harbor': True},
    'TEH': {'name': 'Tehran', 'harbor': False, 'can_harbor': False},
    'TIK': {'name': 'Tiksi', 'harbor': False, 'can_harbor': True},
    'TOK': {'name': 'Tokyo', 'harbor': False, 'can_harbor': True},
    'VAL': {'name': 'Valparaiso', 'harbor': False, 'can_harbor': True},
    'YAK': {'name': 'Yakutsk', 'harbor': False, 'can_harbor': False},
    'VAN': {'name': 'Vancouver', 'harbor': False, 'can_harbor': True},
    'WIN': {'name': 'Winnipeg', 'harbor': False, 'can_harbor': False}
}

tickets_w = [# NA
    ('ANC', 'VAN', 4, 1, 'db'),  
    ('VAN', 'LOS', 1, 1, 'g'),
    ('VAN', 'LOS', 1, 1, 'r'),
    ('VAN', 'WIN', 2, 1, 'y'),
    ('LOS', 'MEX', 2, 1, 'w'),
    ('LOS', 'MEX', 2, 1, 'y'),
    ('LOS', 'NYC', 4, 1, 'p'),
    ('LOS', 'NYC', 4, 1, 'b'),
    ('LOS', 'WIN', 3, 1, 'any'),  # any
    ('WIN', 'NYC', 2, 1, 'g'),
    ('WIN', 'CMB', 4, 1, 'b'),
    ('MIA', 'NYC', 2, 1, 'w'),
    ('MEX', 'CAR', 3, 1, 'r'),
    ('MEX', 'CAR', 3, 1, 'p'),
    ('CAR', 'LIM', 2, 1, 'y'),  
    # SA
    ('CAR', 'LIM', 2, 1, 'w'),
    ('CAR', 'RIO', 4, 1, 'b'),
    ('CAR', 'RIO', 4, 1, 'g'),
    ('LIM', 'VAL', 2, 1, 'any'),  # any
    ('LIM', 'VAL', 2, 1, 'any'),  # any
    ('BUE', 'RIO', 1, 1, 'r'),
    ('BUE', 'RIO', 1, 1, 'w'),
    ('MAR', 'CAS', 2, 1, 'db'),  
    # EUR
    ('MAR', 'HAM', 1, 1, 'p'),
    ('MAR', 'HAM', 1, 1, 'r'),
    ('HAM', 'ATH', 2, 1, 'g'),
    ('HAM', 'MOS', 2, 1, 'b'),
    ('HAM', 'MOS', 2, 1, 'w'),
    ('MUR', 'MOS', 2, 1, 'p'),
    ('ATH', 'TEH', 2, 1, 'any'),  # any
    ('MOS', 'TEH', 3, 1, 'r'),
    ('MOS', 'NOV', 4, 1, 'g'),
    ('MOS', 'NOV', 4, 1, 'y'),
    # AFR
    ('CAS', 'LAG', 4, 1, 'any'),  # any
    ('CAS', 'ALQ', 3, 1, 'any'),  # any
    ('ALQ', 'DJI', 2, 1, 'w'),
    ('ALQ', 'DJI', 2, 1, 'r'),
    ('ALQ', 'TEH', 1, 1, 'b'),
    ('ALQ', 'TEH', 1, 1, 'y'),
    ('LAG', 'LUA', 1, 1, 'p'),
    ('LAG', 'LUA', 1, 1, 'y'),
    ('LUA', 'DES', 4, 1, 'db'),  # db
    ('CPT', 'LUA', 2, 1, 'any'),  # any
    ('CPT', 'DES', 3, 1, 'g'),
    ('CPT', 'DES', 3, 1, 'p'),
    ('DES', 'DJI', 1, 1, 'b'),
    ('DES', 'DJI', 1, 1, 'r'),
    # ASIA
    ('TEH', 'LAH', 4, 1, 'db'),  # db
    ('TEH', 'MUM', 3, 1, 'w'),
    ('TEH', 'MUM', 3, 1, 'p'),
    ('NOV', 'TIK', 3, 1, 'any'),  # any
    ('NOV', 'YAK', 3, 1, 'p'),
    ('NOV', 'BEI', 3, 1, 'r'),
    ('NOV', 'BEI', 3, 1, 'b'),
    ('NOV', 'LAH', 2, 1, 'w'),
    ('TIK', 'YAK', 1, 1, 'g'),
    ('LAH', 'BEI', 6, 1, 'db'),  # db
    ('LAH', 'MUM', 1, 1, 'g'),
    ('LAH', 'MUM', 1, 1, 'b'),
    ('MUM', 'BKK', 3, 1, 'r'),
    ('MUM', 'BKK', 3, 1, 'y'),
    ('YAK', 'PET', 3, 1, 'w'),
    ('YAK', 'BEI', 3, 1, 'y'),
    ('HKG', 'BEI', 2, 1, 'w'),
    ('HKG', 'BEI', 2, 1, 'g'),
    ('BKK', 'HKG', 1, 1, 'p'),
    ('BKK', 'HKG', 1, 1, 'b'),
    # OCE
    ('PER', 'SYD', 2, 1, 'y'),  
    ('PER', 'SYD', 2, 1, 'w'),
    ('DAR', 'PER', 2, 1, 'r'),
    ('SYD', 'DAR', 2, 1, 'g'),
    # (Sea Connections)
    # NA
    ('ANC', 'CMB', 6, 2, 'b'),  
    ('CMB', 'REY', 6, 2, 'w'),
    ('NYC', 'REY', 6, 2, 'y'),
    ('NYC', 'EDI', 7, 2, 'p'),
    ('NYC', 'EDI', 7, 2, 'r'),
    ('MIA', 'CAS', 7, 2, 'g'),
    ('MIA', 'CAR', 2, 2, 'w'),
    # SA
    ('CAR', 'LAG', 7, 2, 'r'),
    ('RIO', 'LUA', 6, 2, 'any'),  # any
    ('RIO', 'CPT', 6, 2, 'w'),
    ('RIO', 'CPT', 6, 2, 'b'),
    ('BUE', 'CPT', 6, 2, 'p'),
    ('BUE', 'CPT', 6, 2, 'y'),
    ('VAL', 'BUE', 3, 2, 'g'),
    # EUR
    ('REY', 'MUR', 4, 2, 'g'),
    ('REY', 'EDI', 2, 2, 'any'),  # any
    ('EDI', 'HAM', 1, 2, 'y'),
    ('EDI', 'HAM', 1, 2, 'b'),
    ('EDI', 'MAR', 1, 2, 'w'),
    ('EDI', 'MAR', 1, 2, 'g'),
    ('MUR', 'TIK', 7, 2, 'r'),
    ('MAR', 'ATH', 2, 2, 'r'),
    ('ATH', 'ALQ', 1, 2, 'g'),
    # AFR + AAO
    ('DES', 'MUM', 4, 2, 'w'),
    ('DES', 'JAK', 7, 2, 'p'),
    ('DES', 'JAK', 7, 2, 'g'),
    ('DES', 'TOA', 1, 2, 'y'),
    ('CPT', 'TOA', 3, 2, 'any'),  # any
    ('CPT', 'AAO', 5, 2, 'g'),
    ('CPT', 'AAO', 5, 2, 'r'),
    ('AAO', 'PER', 5, 2, 'w'),
    ('AAO', 'PER', 5, 2, 'p'),
    # ASIA
    ('TIK', 'ANC', 8, 2, 'y'),
    ('TIK', 'PET', 7, 2, 'b'),
    ('PET', 'ANC', 3, 2, 'p'),
    ('PET', 'TOK', 2, 2, 'any'),  # any
    ('HKG', 'TOK', 3, 2, 'any'),  # any
    ('HKG', 'MAN', 1, 2, 'p'),
    ('BKK', 'JAK', 2, 2, 'r'),
    ('BKK', 'MAN', 2, 2, 'w'),
    ('JAK', 'PER', 3, 2, 'any'),  # any
    ('JAK', 'DAR', 2, 2, 'b'),
    ('JAK', 'MAN', 2, 2, 'any'),  # any
    # OCE
    ('MAN', 'TOK', 2, 2, 'y'),
    ('MAN', 'HON', 5, 2, 'w'),
    ('TOK', 'VAN', 6, 2, 'w'),
    ('TOK', 'LOS', 7, 2, 'b'),
    ('TOK', 'LOS', 7, 2, 'g'),
    ('TOK', 'HON', 5, 2, 'r'),
    ('DAR', 'PTM', 1, 2, 'r'),
    ('PTM', 'HON', 3, 2, 'g'),
    ('SYD', 'PTM', 3, 2, 'y'),
    ('SYD', 'LIM', 8, 2, 'p'),
    ('SYD', 'LIM', 8, 2, 'b'),
    ('SYD', 'CHR', 1, 2, 'r'),
    ('SYD', 'CHR', 1, 2, 'w'),
    ('CHR', 'VAL', 7, 2, 'y'),
    ('HON', 'LOS', 3, 2, 'y')]


city_gl = {
    'BAY': {'name': 'Bay City', 'harbor': False, 'can_harbor': True},
    'SCR': {'name': 'Scranton', 'harbor': False, 'can_harbor': False},
    'BUF': {'name': 'Buffalo', 'harbor': False, 'can_harbor': True},
    'ALB': {'name': 'Albany', 'harbor': False, 'can_harbor': True},
    'CDR': {'name': 'Cedar Rapids', 'harbor': False, 'can_harbor': False},
    'CLE': {'name': 'Cleveland', 'harbor': False, 'can_harbor': True},
    'SSM': {'name': 'Sault Ste. Marie', 'harbor': False, 'can_harbor': True},
    'WAU': {'name': 'Wausau', 'harbor': False, 'can_harbor': False},
    'CHI': {'name': 'Chicago', 'harbor': False, 'can_harbor': True},
    'NYC': {'name': 'New York', 'harbor': False, 'can_harbor': True},
    'TIM': {'name': 'Timmins', 'harbor': False, 'can_harbor': False},
    'TOR': {'name': 'Toronto', 'harbor': False, 'can_harbor': True},
    'MON': {'name': 'Montreal', 'harbor': False, 'can_harbor': True},
    'DET': {'name': 'Detroit', 'harbor': False, 'can_harbor': True},
    'OTT': {'name': 'Ottawa', 'harbor': False, 'can_harbor': False},
    'DUL': {'name': 'Duluth', 'harbor': False, 'can_harbor': True},
    'ROU': {'name': 'Rouyn-Noranda', 'harbor': False, 'can_harbor': False},
    'TRA': {'name': 'Traverse City', 'harbor': False, 'can_harbor': True},
    'EAU': {'name': 'Eau Claire', 'harbor': False, 'can_harbor': False},
    'TOL': {'name': 'Toledo', 'harbor': False, 'can_harbor': True},
    'GBA': {'name': 'Green Bay', 'harbor': False, 'can_harbor': True},
    'MAD': {'name': 'Madison', 'harbor': False, 'can_harbor': False},
    'POR': {'name': 'Port Elgin', 'harbor': False, 'can_harbor': True},
    'MAR': {'name': 'Marathon', 'harbor': False, 'can_harbor': True},
    'SOU': {'name': 'South Bend', 'harbor': False, 'can_harbor': False},
    'ERI': {'name': 'Erie', 'harbor': False, 'can_harbor': True},
    'KIN': {'name': 'Kingston', 'harbor': False, 'can_harbor': True},
    'MIL': {'name': 'Milwaukee', 'harbor': False, 'can_harbor': True},
    'PAR': {'name': 'Parry Sound', 'harbor': False, 'can_harbor': True},
    'MUS': {'name': 'Muskegon', 'harbor': False, 'can_harbor': True},
    'SYR': {'name': 'Syracuse', 'harbor': False, 'can_harbor': True},
    'SUD': {'name': 'Sudbury', 'harbor': False, 'can_harbor': False},
    'THU': {'name': 'Thunder Bay', 'harbor': False, 'can_harbor': True},
    'SBM': {'name': 'South Baymouth', 'harbor': False, 'can_harbor': True},
    'MRQ': {'name': 'Marquette', 'harbor': False, 'can_harbor': True},
    'LKS': {'name': 'Lake Superior', 'harbor': False, 'can_harbor': False},
    'LKH': {'name': 'Lake Huron', 'harbor': False, 'can_harbor': False}
}

def initialize_world():
    world = WeightedGraph()
    #add_edge(node1, node2, weights, type, color)
    
    '''
    Routes facing N-->S, then L -> R by continent. 
    '''
    _land = True
    _sea = True
    ## Land Connections
    if _land:
        # NA
        world.add_edge('ANC', 'VAN', 4, 1, 'db') #db
        world.add_edge('VAN', 'LOS', 1, 1, 'g')
        world.add_edge('VAN', 'LOS', 1, 1, 'r')
        world.add_edge('VAN', 'WIN', 2, 1, 'y')
        world.add_edge('LOS', 'MEX', 2, 1, 'w')
        world.add_edge('LOS', 'MEX', 2, 1, 'y')
        world.add_edge('LOS', 'NYC', 4, 1, 'p')
        world.add_edge('LOS', 'NYC', 4, 1, 'b')
        world.add_edge('LOS', 'WIN', 3, 1, 'any') #any
        world.add_edge('WIN', 'NYC', 2, 1, 'g')
        world.add_edge('WIN', 'CMB', 4, 1, 'b')
        world.add_edge('MIA', 'NYC', 2, 1, 'w')
        world.add_edge('MEX', 'CAR', 3, 1, 'r')
        world.add_edge('MEX', 'CAR', 3, 1, 'p')

        # SA
        world.add_edge('CAR', 'LIM', 2, 1, 'y')
        world.add_edge('CAR', 'LIM', 2, 1, 'w')
        world.add_edge('CAR', 'RIO', 4, 1, 'b')
        world.add_edge('CAR', 'RIO', 4, 1, 'g')
        world.add_edge('LIM', 'VAL', 2, 1, 'any') #any
        world.add_edge('LIM', 'VAL', 2, 1, 'any') #any
        world.add_edge('BUE', 'RIO', 1, 1, 'r')
        world.add_edge('BUE', 'RIO', 1, 1, 'w')

        # EUR
        world.add_edge('MAR', 'CAS', 2, 1, 'db') #any
        world.add_edge('MAR', 'HAM', 1, 1, 'p')
        world.add_edge('MAR', 'HAM', 1, 1, 'r')
        world.add_edge('HAM', 'ATH', 2, 1, 'g')
        world.add_edge('HAM', 'MOS', 2, 1, 'b')
        world.add_edge('HAM', 'MOS', 2, 1, 'w')
        world.add_edge('MUR', 'MOS', 2, 1, 'p')
        world.add_edge('ATH', 'TEH', 2, 1, 'any') #any
        world.add_edge('MOS', 'TEH', 3, 1, 'r')
        world.add_edge('MOS', 'NOV', 4, 1, 'g')
        world.add_edge('MOS', 'NOV', 4, 1, 'y')

        # AFR
        world.add_edge('CAS', 'LAG', 4, 1, 'any') #any
        world.add_edge('CAS', 'ALQ', 3, 1, 'any') #any
        world.add_edge('ALQ', 'DJI', 2, 1, 'w')
        world.add_edge('ALQ', 'DJI', 2, 1, 'r') 
        world.add_edge('ALQ', 'TEH', 1, 1, 'b')
        world.add_edge('ALQ', 'TEH', 1, 1, 'y')        
        world.add_edge('LAG', 'LUA', 1, 1, 'p')
        world.add_edge('LAG', 'LUA', 1, 1, 'y')
        world.add_edge('LUA', 'DES', 4, 1, 'db') #db
        world.add_edge('CPT', 'LUA', 2, 1, 'any') #any
        world.add_edge('CPT', 'DES', 3, 1, 'g')
        world.add_edge('CPT', 'DES', 3, 1, 'p')
        world.add_edge('DES', 'DJI', 1, 1, 'b')
        world.add_edge('DES', 'DJI', 1, 1, 'r')

        # ASIA
        world.add_edge('TEH', 'LAH', 4, 1, 'db') #db
        world.add_edge('TEH', 'MUM', 3, 1, 'w')
        world.add_edge('TEH', 'MUM', 3, 1, 'p')
        world.add_edge('NOV', 'TIK', 3, 1, 'any') #any
        world.add_edge('NOV', 'YAK', 3, 1, 'p')
        world.add_edge('NOV', 'BEI', 3, 1, 'r')
        world.add_edge('NOV', 'BEI', 3, 1, 'b')
        world.add_edge('NOV', 'LAH', 2, 1, 'w')
        world.add_edge('TIK', 'YAK', 1, 1, 'g')
        world.add_edge('LAH', 'BEI', 6, 1, 'db') #db
        world.add_edge('LAH', 'MUM', 1, 1, 'g')
        world.add_edge('LAH', 'MUM', 1, 1, 'b')
        world.add_edge('MUM', 'BKK', 3, 1, 'r')
        world.add_edge('MUM', 'BKK', 3, 1, 'y')
        world.add_edge('YAK', 'PET', 3, 1, 'w')
        world.add_edge('YAK', 'BEI', 3, 1, 'y')
        world.add_edge('HKG', 'BEI', 2, 1, 'w')
        world.add_edge('HKG', 'BEI', 2, 1, 'g')
        world.add_edge('BKK', 'HKG', 1, 1, 'p')
        world.add_edge('BKK', 'HKG', 1, 1, 'b')
        
        # OCE    
        world.add_edge('PER', 'SYD', 2, 1, 'y')
        world.add_edge('PER', 'SYD', 2, 1, 'w')
        world.add_edge('DAR', 'PER', 2, 1, 'r')
        world.add_edge('SYD', 'DAR', 2, 1, 'g')

    ## Sea Connections
    if _sea:
        # NA
        world.add_edge('ANC', 'CMB', 6, 2, 'b')
        world.add_edge('CMB', 'REY', 6, 2, 'w')
        world.add_edge('NYC', 'REY', 6, 2, 'y')
        world.add_edge('NYC', 'EDI', 7, 2, 'p')
        world.add_edge('NYC', 'EDI', 7, 2, 'r')
        world.add_edge('MIA', 'CAS', 7, 2, 'g')
        world.add_edge('MIA', 'CAR', 2, 2, 'w')

        # SA
        world.add_edge('CAR', 'LAG', 7, 2, 'r')
        world.add_edge('RIO', 'LUA', 6, 2, 'any') #any
        world.add_edge('RIO', 'CPT', 6, 2, 'w')
        world.add_edge('RIO', 'CPT', 6, 2, 'b')
        world.add_edge('BUE', 'CPT', 6, 2, 'p')
        world.add_edge('BUE', 'CPT', 6, 2, 'y')
        world.add_edge('VAL', 'BUE', 3, 2, 'g')

        # EUR
        world.add_edge('REY', 'MUR', 4, 2, 'g')
        world.add_edge('REY', 'EDI', 2, 2, 'any') #any
        world.add_edge('EDI', 'HAM', 1, 2, 'y')
        world.add_edge('EDI', 'HAM', 1, 2, 'b')
        world.add_edge('EDI', 'MAR', 1, 2, 'w')
        world.add_edge('EDI', 'MAR', 1, 2, 'g')
        world.add_edge('MUR', 'TIK', 7, 2, 'r')
        world.add_edge('MAR', 'ATH', 2, 2, 'r')
        world.add_edge('ATH', 'ALQ', 1, 2, 'g')

        # AFR
        world.add_edge('DES', 'MUM', 4, 2, 'w')
        world.add_edge('DES', 'JAK', 7, 2, 'p')
        world.add_edge('DES', 'JAK', 7, 2, 'g')
        world.add_edge('DES', 'TOA', 1, 2, 'y')
        world.add_edge('CPT', 'TOA', 3, 2, 'any') #any
        world.add_edge('CPT', 'AAO', 5, 2, 'g')
        world.add_edge('CPT', 'AAO', 5, 2, 'r')

        # (*) Transit Spot
        world.add_edge('AAO', 'PER', 5, 2, 'w')
        world.add_edge('AAO', 'PER', 5, 2, 'p')

        # ASIA
        world.add_edge('TIK', 'ANC', 8, 2, 'y')
        world.add_edge('TIK', 'PET', 7, 2, 'b')
        world.add_edge('PET', 'ANC', 3, 2, 'p')
        world.add_edge('PET', 'TOK', 2, 2, 'any') #any
        world.add_edge('HKG', 'TOK', 3, 2, 'any') #any
        world.add_edge('HKG', 'MAN', 1, 2, 'p')
        world.add_edge('BKK', 'JAK', 2, 2, 'r')
        world.add_edge('BKK', 'MAN', 2, 2, 'w')

        # OCE
        world.add_edge('JAK', 'PER', 3, 2, 'any') #any
        world.add_edge('JAK', 'DAR', 2, 2, 'b')
        world.add_edge('JAK', 'MAN', 2, 2, 'any') #any
        world.add_edge('MAN', 'TOK', 2, 2, 'y')
        world.add_edge('MAN', 'HON', 5, 2, 'w')
        world.add_edge('TOK', 'VAN', 6, 2, 'w')
        world.add_edge('TOK', 'LOS', 7, 2, 'b')
        world.add_edge('TOK', 'LOS', 7, 2, 'g')
        world.add_edge('TOK', 'HON', 5, 2, 'r')
        world.add_edge('DAR', 'PTM', 1, 2, 'r')
        world.add_edge('PTM', 'HON', 3, 2, 'g')
        world.add_edge('SYD', 'PTM', 3, 2, 'y')
        world.add_edge('SYD', 'LIM', 8, 2, 'p')
        world.add_edge('SYD', 'LIM', 8, 2, 'b')
        world.add_edge('SYD', 'CHR', 1, 2, 'r')
        world.add_edge('SYD', 'CHR', 1, 2, 'w')
        world.add_edge('CHR', 'VAL', 7, 2, 'y')
        world.add_edge('HON', 'LOS', 3, 2, 'y')

    return world

def initialize_world_tickets():
    tix = DestinationTickets()
    # <10
    tix.add_ticket(DestinationTicket('ALQ', 'MAR', 5))
    tix.add_ticket(DestinationTicket('JAK', 'HKG', 5))
    tix.add_ticket(DestinationTicket('RIO', 'VAL', 6))
    tix.add_ticket(DestinationTicket('BEI', 'MUM', 6))
    tix.add_ticket(DestinationTicket('SYD', 'JAK', 7))
    tix.add_ticket(DestinationTicket('LAH', 'DJI', 7))
    tix.add_ticket(DestinationTicket('DES', 'HAM', 8))
    tix.add_ticket(DestinationTicket('BUE', 'MIA', 9))
    tix.add_ticket(DestinationTicket('MIA', 'VAN', 9))

    # <15
    tix.add_ticket(DestinationTicket('LUA', 'EDI', 10))
    tix.add_ticket(DestinationTicket('MAR', 'NYC', 10))
    tix.add_ticket(DestinationTicket('TEH', 'LAG', 10))
    tix.add_ticket(DestinationTicket('SYD', 'TOK', 11))
    tix.add_ticket(DestinationTicket('DES', 'RIO', 11))
    tix.add_ticket(DestinationTicket('TOA', 'MOS', 11))
    tix.add_ticket(DestinationTicket('NYC', 'MEX', 11))
    tix.add_ticket(DestinationTicket('JAK', 'LOS', 11)) 
    tix.add_ticket(DestinationTicket('ATH', 'CAR', 12))
    tix.add_ticket(DestinationTicket('MOS', 'MIA', 13))
    tix.add_ticket(DestinationTicket('HKG', 'MOS', 13))
    tix.add_ticket(DestinationTicket('EDI', 'VAN', 13))
    tix.add_ticket(DestinationTicket('DRW', 'NOV', 13))
    tix.add_ticket(DestinationTicket('MUM', 'REY', 13))
    tix.add_ticket(DestinationTicket('BEI', 'HAM', 13))
    tix.add_ticket(DestinationTicket('BEI', 'MEX', 13))
    tix.add_ticket(DestinationTicket('PER', 'WIN', 14))
    tix.add_ticket(DestinationTicket('BEI', 'MAR', 14))
    tix.add_ticket(DestinationTicket('HKG', 'LAG', 14))
    tix.add_ticket(DestinationTicket('JAK', 'LIM', 14))
    tix.add_ticket(DestinationTicket('HAM', 'LOS', 14))

    # <20
    tix.add_ticket(DestinationTicket('RIO', 'LOS', 15))
    tix.add_ticket(DestinationTicket('PET', 'MOS', 15))
    tix.add_ticket(DestinationTicket('MUM', 'MEX', 15))
    tix.add_ticket(DestinationTicket('CAR', 'MEX', 15))
    tix.add_ticket(DestinationTicket('TOK', 'NYC', 15))    
    tix.add_ticket(DestinationTicket('TOK', 'DES', 15))
    tix.add_ticket(DestinationTicket('HON', 'CAS', 16))
    tix.add_ticket(DestinationTicket('VAK', 'CAS', 16))
    tix.add_ticket(DestinationTicket('HKG', 'EDI', 17))
    tix.add_ticket(DestinationTicket('DES', 'LOS', 17))
    tix.add_ticket(DestinationTicket('SYD', 'NYC', 17))
    tix.add_ticket(DestinationTicket('PER', 'RIO', 17))
    tix.add_ticket(DestinationTicket('HAM', 'RIO', 18))
    tix.add_ticket(DestinationTicket('JAK', 'MAR', 18))
    tix.add_ticket(DestinationTicket('CPT', 'NYC', 19))
    tix.add_ticket(DestinationTicket('MUM', 'NYC', 19))
    # <max    
    tix.add_ticket(DestinationTicket('TOK', 'RIO', 20))
    tix.add_ticket(DestinationTicket('TOK', 'EDI', 22))
    tix.add_ticket(DestinationTicket('CHR', 'MAR', 23))
    tix.add_ticket(DestinationTicket('SYD', 'EDI', 25))

    return tix

## initialize great lakes ## --------------------------------------------------------------

def initialize_gl():
    gl = WeightedGraph()
    #add_edge(node1, node2, weights, type, color)
    
    '''
    Routes facing N-->S, then L -> R by continent. 
    '''
    _land = True
    _sea = True
    ## Land Connections
    if _land:
        # West
        gl.add_edge('DUL', 'THU', 5, 1, 'b')
        gl.add_edge('DUL', 'WAU', 4, 1, 'g')
        gl.add_edge('DUL', 'EAU', 3, 1, 'y')
        gl.add_edge('EAU', 'CDR', 5, 1, 'p')
        gl.add_edge('EAU', 'MAD', 4, 1, 'w')
        gl.add_edge('EAU', 'WAU', 2, 1, 'any')
        gl.add_edge('WAU', 'MRQ', 4, 1, 'w')
        gl.add_edge('WAU', 'GBA', 1, 1, 'r')
        gl.add_edge('WAU', 'MIL', 4, 1, 'b')
        gl.add_edge('WAU', 'MAD', 4, 1, 'p')
        gl.add_edge('CDR', 'MAD', 3, 1, 'g')
        gl.add_edge('CDR', 'CHI', 4, 1, 'y')
        gl.add_edge('CDR', 'CHI', 4, 1, 'r')
        gl.add_edge('MAD', 'MIL', 1, 1, 'any')
        gl.add_edge('MAD', 'CHI', 3, 1, 'any')
        gl.add_edge('CHI', 'SOU', 1, 1, 'any')
        gl.add_edge('CHI', 'SOU', 1, 1, 'any')

        # Mid
        gl.add_edge('MAR', 'TIM', 5, 1, 'y')
        gl.add_edge('TRA', 'BAY', 3, 1, 'r')
        gl.add_edge('TRA', 'MUS', 3, 1, 'w')
        gl.add_edge('MUS', 'SOU', 3, 1, 'y')
        gl.add_edge('SOU', 'DET', 4, 1, 'b')
        gl.add_edge('SOU', 'TOL', 3, 1, 'any')
        gl.add_edge('SOU', 'TOL', 3, 1, 'p')
        gl.add_edge('BAY', 'DET', 2, 1, 'g')
        gl.add_edge('DET', 'TOR', 5, 1, 'r')
        gl.add_edge('CLE', 'NYC', 9, 1, 'any')

        # East
        gl.add_edge('TIM', 'ROU', 4, 1, 'g')
        gl.add_edge('SUD', 'SBM', 2, 1, 'any')
        gl.add_edge('SUD', 'PAR', 2, 1, 'any')
        gl.add_edge('SUD', 'TIM', 4, 1, 'w')
        gl.add_edge('SUD', 'TIM', 4, 1, 'r')
        gl.add_edge('SUD', 'OTT', 7, 1, 'g')
        gl.add_edge('SUD', 'OTT', 7, 1, 'b')
        gl.add_edge('SUD', 'ROU', 4, 1, 'p')
        gl.add_edge('TOR', 'POR', 2, 1, 'w')
        gl.add_edge('TOR', 'PAR', 2, 1, 'b')
        gl.add_edge('OTT', 'KIN', 2, 1, 'y')
        gl.add_edge('OTT', 'ROU', 7, 1, 'r')
        gl.add_edge('OTT', 'MON', 1, 1, 'any')
        gl.add_edge('OTT', 'MON', 1, 1, 'any')
        gl.add_edge('MON', 'ROU', 8, 1, 'any')
        gl.add_edge('MON', 'ALB', 5, 1, 'w')
        gl.add_edge('MON', 'ALB', 5, 1, 'g')
        gl.add_edge('SYR', 'KIN', 2, 1, 'p')
        gl.add_edge('SCR', 'SYR', 2, 1, 'w')
        gl.add_edge('SCR', 'SYR', 2, 1, 'b')
        gl.add_edge('SCR', 'BUF', 4, 1, 'any')
        gl.add_edge('SCR', 'ERI', 6, 1, 'y')
        gl.add_edge('SCR', 'ERI', 6, 1, 'p')
        gl.add_edge('SCR', 'NYC', 1, 1, 'g')
        gl.add_edge('SCR', 'MYC', 1, 1, 'r')

    ## Lake Connections
    if _sea:
        # West (of SSM)
        gl.add_edge('THU', 'MAR', 3, 2, 'p')
        gl.add_edge('THU', 'DUL', 4, 2, 'y')
        gl.add_edge('MAR', 'DUL', 6, 2, 'r')
        gl.add_edge('MAR', 'LKS', 2, 2, 'any')
        gl.add_edge('LKS', 'THU', 1, 2, 'any')
        gl.add_edge('LKS', 'THU', 1, 2, 'any')
        gl.add_edge('LKS', 'DUL', 5, 2, 'b')
        gl.add_edge('LKS', 'DUL', 5, 2, 'p')
        gl.add_edge('LKS', 'MAR', 2, 2, 'w')
        gl.add_edge('TRA', 'MUS', 3, 2, 'r')
        gl.add_edge('TRA', 'GBA', 3, 2, 'g')
        gl.add_edge('MIL', 'MUS', 2, 2, 'any')
        gl.add_edge('MIL', 'GBA', 3, 2, 'y')
        gl.add_edge('MIL', 'GBA', 3, 2, 'b')
        gl.add_edge('CHI', 'MUS', 3, 2, 'p')
        gl.add_edge('CHI', 'MIL', 1, 2, 'w')
        gl.add_edge('CHI', 'MIL', 1, 2, 'g')
        gl.add_edge('SSM', 'LKS', 5, 2, 'r')
        gl.add_edge('SSM', 'LKS', 5, 2, 'g')
        gl.add_edge('SSM', 'MAR', 4, 2, 'any')
        gl.add_edge('SSM', 'GBA', 6, 2, 'any')
        gl.add_edge('SSM', 'GBA', 6, 2, 'any')
        gl.add_edge('SSM', 'MRQ', 3, 2, 'any')
        gl.add_edge('SSM', 'TRA', 3, 2, 'any')

        # East (of SSM)
        gl.add_edge('LKH', 'SSM', 4, 2, 'w')
        gl.add_edge('LKH', 'SSM', 4, 2, 'y')
        gl.add_edge('LKH', 'BAY', 2, 2, 'any')
        gl.add_edge('LKH', 'DET', 4, 2, 'b')
        gl.add_edge('LKH', 'DET', 4, 2, 'g')
        gl.add_edge('LKH', 'POR', 1, 2, 'any')
        gl.add_edge('LKH', 'SBM', 1, 2, 'any')
        gl.add_edge('SBM', 'SSM', 3, 2, 'any')
        gl.add_edge('SBM', 'POR', 2, 2, 'any')
        gl.add_edge('SBM', 'PAR', 2, 2, 'w')
        gl.add_edge('POR', 'PAR', 2, 2, 'y')
        gl.add_edge('DET', 'TOL', 1, 2, 'any')
        gl.add_edge('DET', 'TOL', 1, 2, 'any')
        gl.add_edge('DET', 'CLE', 2, 2, 'y')
        gl.add_edge('DET', 'BUF', 6, 2, 'p')
        gl.add_edge('DET', 'BUF', 6, 2, 'w')
        gl.add_edge('CLE', 'TOL', 2, 2, 'w')
        gl.add_edge('CLE', 'TOL', 2, 2, 'r')
        gl.add_edge('CLE', 'ERI', 1, 2, 'b')
        gl.add_edge('CLE', 'ERI', 1, 2, 'g')
        gl.add_edge('KIN', 'MON', 3, 2, 'y')
        gl.add_edge('KIN', 'MON', 3, 2, 'g')
        gl.add_edge('KIN', 'TOR', 4, 2, 'b')
        gl.add_edge('KIN', 'TOR', 4, 2, 'w')
        gl.add_edge('BUF', 'TOR', 1, 2, 'any')
        gl.add_edge('BUF', 'TOR', 1, 2, 'any')
        gl.add_edge('BUF', 'ERI', 2, 2, 'any')
        gl.add_edge('BUF', 'SYR', 3, 2, 'y')
        gl.add_edge('BUF', 'SYR', 3, 2, 'r')
        gl.add_edge('ALB', 'SYR', 2, 2, 'g')
        gl.add_edge('ALB', 'SYR', 2, 2, 'p')
        gl.add_edge('ALB', 'NYC', 3, 2, 'r')
        gl.add_edge('ALB', 'NYC', 3, 2, 'b')


    return gl

def initialize_gl_tickets():
    tix = DestinationTickets()

    # <10
    tix.add_ticket(DestinationTicket('Eau Claire', 'Green Bay', 3))
    tix.add_ticket(DestinationTicket('Erie', 'Kingston', 4))
    tix.add_ticket(DestinationTicket('Buffalo', 'Albany', 4))
    tix.add_ticket(DestinationTicket('Cleveland', 'Toronto', 4))
    tix.add_ticket(DestinationTicket('Erie', 'Kingston', 4))
    tix.add_ticket(DestinationTicket('Sault Ste. Marie', 'Sudbury', 4))
    tix.add_ticket(DestinationTicket('South Baymouth', 'Detroit', 4))
    tix.add_ticket(DestinationTicket('Port Elgin', 'Kingston', 5))
    tix.add_ticket(DestinationTicket('Syracuse', 'Montreal', 5))
    tix.add_ticket(DestinationTicket('Syracuse', 'New York', 5))
    tix.add_ticket(DestinationTicket('Toronto', 'Ottawa', 5))
    tix.add_ticket(DestinationTicket('Green Bay', 'Chicago', 5))
    tix.add_ticket(DestinationTicket('Chicago', 'Detroit', 6))
    tix.add_ticket(DestinationTicket('Perry Sound', 'Rouyn-Noranda', 6))
    tix.add_ticket(DestinationTicket('Traverse City', 'Toledo', 6))
    tix.add_ticket(DestinationTicket('Muskegon', 'Bay City', 6))
    tix.add_ticket(DestinationTicket('Cleveland', 'Ottawa', 7))
    tix.add_ticket(DestinationTicket('Cedar Rapids', 'Wausau', 7))
    tix.add_ticket(DestinationTicket('Milwaukee', 'Erie', 7))
    tix.add_ticket(DestinationTicket('Duluth', 'Traverse City', 7))
    tix.add_ticket(DestinationTicket('Marquette', 'Buffalo', 8))
    tix.add_ticket(DestinationTicket('Milwaukee', 'Perry Sound', 8))
    tix.add_ticket(DestinationTicket('Milwaukee', 'Marquette', 8))
    tix.add_ticket(DestinationTicket('Sault Ste. Marie', 'Syracuse', 8))
    tix.add_ticket(DestinationTicket('Toledo', 'Scranton', 8))
    tix.add_ticket(DestinationTicket('Montreal', 'New York', 9))
    tix.add_ticket(DestinationTicket('Thunder Bay', 'Toronto', 9))
    tix.add_ticket(DestinationTicket('South Bend', 'Syracuse', 9))
    tix.add_ticket(DestinationTicket('Muskegon', 'Buffalo', 9))
    tix.add_ticket(DestinationTicket('Bay City', 'Scranton', 9))
    tix.add_ticket(DestinationTicket('Green Bay', 'Toronto', 9))
 
    # <20   
    tix.add_ticket(DestinationTicket('Duluth', 'Chicago', 10))
    tix.add_ticket(DestinationTicket('Cedar Rapids', 'Sault Ste. Marie', 10))
    tix.add_ticket(DestinationTicket('Marathon', 'Cleveland', 10))
    tix.add_ticket(DestinationTicket('Madison', 'Port Elgin', 10))
    tix.add_ticket(DestinationTicket('Wausau', 'Sudbury', 10))
    tix.add_ticket(DestinationTicket('Marquette', 'Albany', 10))
    tix.add_ticket(DestinationTicket('Chicago', 'Toronto', 11))
    tix.add_ticket(DestinationTicket('Cedar Rapids', 'Cleveland', 11))
    tix.add_ticket(DestinationTicket('Marathon', 'South Bend', 11))
    tix.add_ticket(DestinationTicket('Detroit', 'Montreal', 11))
    tix.add_ticket(DestinationTicket('Sudbury', 'New York', 12))
    tix.add_ticket(DestinationTicket('Detroit', 'New York', 12))
    tix.add_ticket(DestinationTicket('Duluth', 'Detroit', 12))
    tix.add_ticket(DestinationTicket('Eau Claire', 'Toledo', 12))
    tix.add_ticket(DestinationTicket('Green Bay', 'Timmins', 13))
    tix.add_ticket(DestinationTicket('Sault Ste. Marie', 'Montreal', 13))
    tix.add_ticket(DestinationTicket('Duluth', 'Rouyn-Noranda', 14))
    tix.add_ticket(DestinationTicket('Chicago', 'New York', 15))
    tix.add_ticket(DestinationTicket('Chicago', 'Timmins', 15))
    tix.add_ticket(DestinationTicket('Chicago', 'Montreal', 16))
    tix.add_ticket(DestinationTicket('Cedar Rapids', 'Albany', 16))
    tix.add_ticket(DestinationTicket('Thunder Bay', 'Ottawa', 17))
    tix.add_ticket(DestinationTicket('Madison', 'Ottawa', 18))
    tix.add_ticket(DestinationTicket('Duluth', 'Montreal', 19))
    # <max
    tix.add_ticket(DestinationTicket('Duluth', 'New York', 24))

    return tix


## define iterations ##--------------------------------------------------------------------------------
def ships(num):
    ways = []

    if num==1:
        ways=[[1]]
        return ways
    
    max_twos = num//2 #floor twos

    for i in range(1+max_twos):
        way=[]
        if num%2==1:
            way.append(1)
        for two in range(i): # add max number of twos
            way.append(2)
        for one in range(num-sum(way)):
            way.append(1)
        ways.append(way)
    return ways

def len_ways(ways):
    len_ways=[]
    for i in ways:
        len_ways.append(len(i))
    return len_ways

def print_iteration(i):
    ans = ships(i)
    print(f"{i}:[{len(ans)}]")
    for j in ans:
        print(f"-->( {len(j)} )={j}")

def nothing():
    i=0
    i+1

def bezier_curve(p0, p1, p2, t):
    return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2

def graph3D(graph, cities, tickets):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')



    # add cities
    for id, city in cities.items():
        graph.add_node(id, name=city['name'], has_harbor=city['harbor'], can_harbor=city['can_harbor'])

    # add routes
    for edge in functions.tickets_w:
        city1, city2, weight, _type, color = edge
        graph.add_edge(city1, city2, weight=weight, _type=_type, color=functions.colors[color])

    # get pos from viz
    pos = nx.spring_layout(graph, dim=3, seed=70)

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
    for edge in graph.edges(data=True):

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