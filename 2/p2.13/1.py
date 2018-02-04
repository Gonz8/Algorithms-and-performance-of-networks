class FIFO:
    def __init__(self):
        self.list = []
        self.size = 0

    def insert(self, x):
        self.list.append(x)
        self.size += 1

    def getFirst(self):
        aux = self.list[0]
        del self.list[0]
        self.size -= 1
        return aux

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    '''
    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])
    '''
    def add_neighbor(self, neighbor, relation):
        self.adjacent[neighbor] = relation

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_relation(self, adj):
        return self.adjacent[adj]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0
    '''
    def __iter__(self):
        return iter(self.vert_dict.values())
    '''

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, relation):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], relation)

    def get_vertices(self):
        return self.vert_dict.keys()

def get_route(_AS, _neighbor, _r):
    link = _neighbor.get_relation(_AS) # link type of neighbor in respect to AS
    exported_route = _r[_AS.id] # exported route
    route = None
    if link == 1: # Export to provider
        if exported_route == 'c': # exported route = costumer
            route = 'c'
    elif link == 2: # Export to peer
        if exported_route == 'c': # exported route = costumer
            route = 'r'
    else: # Export to costumer
        if exported_route != None: # exported route = costumer or peer or provider
            route = 'p'
    return route

# Checks if the new route is better than the current one by this order: c < r < p < None(bullet).
# Outputs True if is better and False otherwise
def better_route(_neighbor, _new_route, _AS, _r):
    answer = False
    route = _r[_neighbor] # Current vertex route type

    if route == 'r' and _new_route == 'c':
        answer = True
    elif route == 'p' and (_new_route == 'c' or _new_route == 'r'):
        answer = True
    elif route == None and _new_route != None:
        answer = True
    return answer

def elect_route(graph, destination, r):

    Q = FIFO()
    r[destination] = 'c'
    Q.insert(graph.vert_dict[destination])

    # while
    while(Q.size > 0):

        AS = Q.getFirst()
        for neighbor in graph.vert_dict[AS.id].get_connections():

            new_route = get_route(AS, neighbor, r) # Gets the new tpe of route when exported by the AS to a neighbor
            if better_route(neighbor.id, new_route, AS.id, r): # If the new exported route is better that the previous one in neighbor
                r[neighbor.id] = new_route
                Q.insert(neighbor)

    return

if __name__ == '__main__':
    import sys
    import time as t

    Network = Graph()

    # Reads the text file and creates the network graph.
    f = open(str(sys.argv[1]),"r")
    for line in f:
        word = line.split()
        Network.add_edge(word[0], word[1], int(word[2]))

    f.closed

    # Asks user for destination id
    while True:
        destination = input("\nInput a destination id: ")
        if destination not in tuple(Network.get_vertices()):
            print("Not a valid destination.\n")
        else:
            break

    # Initialization of route types
    route = {}
    for vertex in Network.vert_dict:
        route[vertex] = None

    now = t.time()
    # Computes the type of commercial route (provider, peer, customer, or unusable)
    elect_route(Network, destination, route)
    deltat = t.time() - now
    print('Computation time of elected route: ', deltat)



    # Asks user for an AS id to show the type of route
    while True:
        AS = input("\nInput a start id: ")
        if AS not in tuple(Network.get_vertices()):
            print("Not a valid AS id.\n")
        else:
            break

    # Prints the type of route of the wanted AS
    input_ = route[AS] # inputted AS
    if input_ == 'c':
        print('\nType of commercial route: customer')
    elif input_ == 'r':
        print('\nType of commercial route: peer')
    elif input_ == 'p':
        print('\nType of commercial route: provider')
    elif input_ == None:
        print('\nType of commercial route: unusable')
