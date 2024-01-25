# Helper functions for ticket-to-ride optimizer #
# 
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
    'BKK': {'name': 'Bangkok', 'harbor': False, 'can_harbor': True},
    'BUE': {'name': 'Buenos Aires', 'harbor': False, 'can_harbor': True},
    'CAR': {'name': 'Caracas', 'harbor': False, 'can_harbor': True},
    'CAS': {'name': 'Casablanca', 'harbor': False, 'can_harbor': True},
    'CMB': {'name': 'Cambridge Bay', 'harbor': False, 'can_harbor': True},
    'CPT': {'name': 'Cape Town', 'harbor': False, 'can_harbor': True},
    'CHR': {'name': 'Christchurch', 'harbor': False, 'can_harbor': True},
    'DES': {'name': 'Dar Es Salaam', 'harbor': False, 'can_harbor': True},
    'DJI': {'name': 'Djibouti', 'harbor': False, 'can_harbor': True},
    'EDI': {'name': 'Edinburgh', 'harbor': False, 'can_harbor': True},
    'HAM': {'name': 'Hamburg', 'harbor': False, 'can_harbor': True},
    'HKG': {'name': 'Hong Kong', 'harbor': False, 'can_harbor': True},
    'HON': {'name': 'Honolulu', 'harbor': False, 'can_harbor': True},
    'JAK': {'name': 'Jakarta', 'harbor': False, 'can_harbor': True},
    'LAH': {'name': 'Lahore', 'harbor': False, 'can_harbor': True},
    'LAG': {'name': 'Lagos', 'harbor': False, 'can_harbor': True},
    'LIM': {'name': 'Lima', 'harbor': False, 'can_harbor': True},
    'LOS': {'name': 'Los Angeles', 'harbor': False, 'can_harbor': True},
    'LUA': {'name': 'Luanda', 'harbor': False, 'can_harbor': True},
    'MAN': {'name': 'Manila', 'harbor': False, 'can_harbor': True},
    'MAR': {'name': 'Marseille', 'harbor': False, 'can_harbor': True},
    'MEX': {'name': 'Mexico', 'harbor': False, 'can_harbor': True},
    'MIA': {'name': 'Miami', 'harbor': False, 'can_harbor': True},
    'MOS': {'name': 'Moskva', 'harbor': False, 'can_harbor': True},
    'MUM': {'name': 'Mumbai', 'harbor': False, 'can_harbor': True},
    'NOV': {'name': 'Novosibirsk', 'harbor': False, 'can_harbor': True},
    'NYC': {'name': 'New York', 'harbor': False, 'can_harbor': True},
    'PER': {'name': 'Perth', 'harbor': False, 'can_harbor': True},
    'PET': {'name': 'Petropavlovsk', 'harbor': False, 'can_harbor': True},
    'PTM': {'name': 'Port Moresby', 'harbor': False, 'can_harbor': True},
    'TOA': {'name': 'Toamasina', 'harbor': False, 'can_harbor': True},
    'REY': {'name': 'Reykjavik', 'harbor': False, 'can_harbor': True},
    'RIO': {'name': 'Rio De Janeiro', 'harbor': False, 'can_harbor': True},
    'SYD': {'name': 'Sydney', 'harbor': False, 'can_harbor': True},
    'TOA': {'name': 'Toamasina', 'harbor': False, 'can_harbor': True},
    'TEH': {'name': 'Tehran', 'harbor': False, 'can_harbor': True},
    'TIK': {'name': 'Tiksi', 'harbor': False, 'can_harbor': True},
    'TOK': {'name': 'Tokyo', 'harbor': False, 'can_harbor': True},
    'VAL': {'name': 'Valparaiso', 'harbor': False, 'can_harbor': True},
    'YAK': {'name': 'Yakutsk', 'harbor': False, 'can_harbor': True},
    'VAN': {'name': 'Vancouver', 'harbor': False, 'can_harbor': True},
    'WIN': {'name': 'Winnipeg', 'harbor': False, 'can_harbor': True}
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
    'BAY': {'name': 'Bay City', 'harbor': False, 'can_harbor':True},
    'SCR': 'Scranton',
    'BUF': 'Buffalo',
    'ALB': 'Albany',
    'CDR': 'Cedar Rapids',
    'CLE': 'Cleveland',
    'SSM': 'Sault Ste. Marie',
    'WAU': 'Wausau',
    'CHI': 'Chicago',
    'NYC': 'New York',
    'TIM': 'Timmins',
    'TOR': 'Toronto',
    'MON': 'Montreal',
    'DET': 'Detroit',
    'OTT': 'Ottawa',
    'DUL': 'Duluth',
    'ROU': 'Rouyn-Noranda',
    'TRA': 'Traverse City',
    'EAU': 'Eau Claire',
    'TOL': 'Toledo',
    'GBA': 'Green Bay',
    'MAD': 'Madison',
    'POR': 'Port Elgin',
    'MAR': 'Marathon',
    'SOU': 'South Bend',
    'ERI': 'Erie',
    'KIN': 'Kingston',
    'MIL': 'Milwaukee',
    'PER': 'Perry Sound',
    'MUS': 'Muskegon',
    'SYR': 'Syracuse',
    'SUD': 'Sudbury',
    'THU': 'Thunder Bay',
    'SBM': 'South Baymouth'
}

def initialize_world():
    world = WeightedGraph()
    #add_edge(node1, node2, weights, type, color)
    
    '''
    Routes facing N-->S, then L -> R by continent. 
    '''

    ## Land Connections
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
    #TODO: Consider double ship cards
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
    tix.add_ticket(DestinationTicket('TOK', 'RIO', 20))

    # <max
    tix.add_ticket(DestinationTicket('TOK', 'EDI', 22))
    tix.add_ticket(DestinationTicket('CHR', 'MAR', 23))
    tix.add_ticket(DestinationTicket('SYD', 'EDI', 25))

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