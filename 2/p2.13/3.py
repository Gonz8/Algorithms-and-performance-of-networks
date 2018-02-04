class BinHeap:
	def __init__(self):
        	self.heapList = [[-1, 'None']]
        	self.currentSize = 0

	def percUp(self,i):
		while i // 2 > 0:
	      		if self.heapList[i][0] < self.heapList[i // 2][0]:
	         		tmp = self.heapList[i // 2]
	         		self.heapList[i // 2] = self.heapList[i]
	         		self.heapList[i] = tmp
	      		i = i // 2

	def insert(self,k):
	    	self.heapList.append(k)
	    	self.currentSize = self.currentSize + 1
	    	self.percUp(self.currentSize)

	def percDown(self,i):
    		while (i * 2) <= self.currentSize:
        		mc = self.minChild(i)
        		if self.heapList[i][0] > self.heapList[mc][0]:
            			tmp = self.heapList[i]
            			self.heapList[i] = self.heapList[mc]
            			self.heapList[mc] = tmp
        		i = mc

	def minChild(self,i):
	    	if i * 2 + 1 > self.currentSize:
	        	return i * 2
	    	else:
	        	if self.heapList[i*2][0] < self.heapList[i*2+1][0]:
	        		return i * 2
	        	else:
	        		return i * 2 + 1

	def delMin(self):
	    	retval = self.heapList[1]
	    	self.heapList[1] = self.heapList[self.currentSize]
	    	self.currentSize = self.currentSize - 1
	    	self.heapList.pop() #del self.heapList[self.currentSize]
	    	self.percDown(1)
	    	return retval[1]

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
# If the type of roots are the same he considers the route with less hops.
# Outputs True if is better and False otherwise
def better_route(_neighbor, _new_route, _AS, _r, _h):
    answer = False
    route = _r[_neighbor] # Current vertex route type

    if (route == _new_route) and (_h[_AS] + 1 < _h[_neighbor]) and (route != None):
        answer = True
    elif route == 'r' and _new_route == 'c':
        answer = True
    elif route == 'p' and (_new_route == 'c' or _new_route == 'r'):
        answer = True
    elif route == None and _new_route != None:
        answer = True
    return answer

def elect_route(graph, destination, h, r):

    Q = FIFO()
    r[destination] = 'c'
    h[destination] = 0
    Q.insert(graph.vert_dict[destination])

    # while
    while(Q.size > 0):

        AS = Q.getFirst()
        for neighbor in graph.vert_dict[AS.id].get_connections():

            new_route = get_route(AS, neighbor, r) # Gets the new tpe of route when exported by the AS to a neighbor
            if better_route(neighbor.id, new_route, AS.id, r, h): # If the new exported route is better that the previous one in neighbor considering also the number of hops
                r[neighbor.id] = new_route
                h[neighbor.id] =  h[AS.id] + 1
                Q.insert(neighbor)

    return h, r

def Dijkstra(graph, _destination, _dist, _previous):

    Q = BinHeap() # priority queue

    # sets the distance from destination to himself as 0 and inserts in the queue
    _dist[_destination] = 0
    Q.insert([_dist[_destination], _destination])

    # while
    while(Q.currentSize > 0):

        u = Q.delMin()
        for neighbor in graph.vert_dict[u].get_connections():

            alt = _dist[u] + 1
            if alt < _dist[neighbor.id]:
                _dist[neighbor.id] = alt
                Q.insert([_dist[neighbor.id], neighbor.id])
                _previous[neighbor.id] = u

    return _dist

if __name__ == '__main__':
    import sys
    import matplotlib.pyplot as plt
    import time as t
    import copy

    Network = Graph()

    print('Reading file...', end = ' ')
    # Reads the text file and creates the network graph.
    f = open(str(sys.argv[1]),"r")
    for line in f:
        word = line.split()
        Network.add_edge(word[0], word[1], int(word[2]))

    f.closed
    print('Done!')

    # Initialization of hops and route types
    inf = float("inf") # define infinity
    hops = {}
    route = {}
    for vertex in Network.vert_dict:
        hops[vertex] = inf
        route[vertex] = None

    num_vert = 0
    best_paths = []
    # Computes the type of commercial route (provider, peer, customer, or unusable) elected at every node to reach the destination for every node
    for vertex in Network.vert_dict:
        now = t.time()
        h, r = elect_route(Network, vertex, copy.copy(hops), copy.copy(route))
        best_paths.append(h)
        deltat = t.time() - now
        print('Computation time of elected routes: ', deltat)
        num_vert += 1

    _max = num_vert # max number of hops to be presented in graph

    # Initialization of hops and route types
    dist = {}
    previous = {}
    for vertex in Network.get_vertices():
        dist[vertex] = inf
        previous[vertex] = None

    shortest_paths = []
    # Computes the shortest path of every node to every node
    for vertex in Network.vert_dict:
        now = t.time()
        h = Dijkstra(Network, vertex, copy.copy(dist), copy.copy(previous))
        shortest_paths.append(h)
        deltat = t.time() - now
        print('Computation time of shortest path: ', deltat)

    # Count number of hops
    hops1 = [0] * (_max + 1)
    for h in best_paths:
        for vertex in Network.get_vertices():
            if h[vertex] == inf:
                continue
            hops1[h[vertex]] += 1

    hops2 = [0] * (_max + 1)
    for h in shortest_paths:
        for vertex in Network.get_vertices():
            hops2[h[vertex]] += 1

	# Cumulative part
    for x in range(_max - 1, 0, -1):
        hops1[x] += hops1[x+1]
        hops2[x] += hops2[x+1]


	# Plot hops in elected routes and shortest paths
    plt.figure(1)

    plt.subplot(211)
    plt.plot(list(range(1, _max + 1)), hops1[1:])
    plt.title('Hops in elected routes')
    plt.ylabel('comulative number of paths')
    plt.xlabel('hops')

    plt.subplot(212)
    plt.plot(list(range(1, _max + 1)), hops2[1:])
    plt.title('Hops in shortest paths')
    plt.ylabel('comulative number of paths')
    plt.xlabel('hops')
    plt.show()



    '''
    # Asks user for destination id
    while True:
        destination = input("\nInput a destination id: ")
        if destination not in tuple(Network.get_vertices()):
            print("Not a valid destination.\n")
        else:
            break

    #r, h = elect_route(Network, destination, copy.copy(hops), copy.copy(route))

    # Asks user for an AS id to show the type of route
    while True:
        AS = input("\nInput a start id: ")
        if AS not in tuple(Network.get_vertices()):
            print("Not a valid AS id.\n")
        else:
            break


    # Prints the type of route of the wanted AS
    for x in best_paths:
        if destination == x[0]:
            r1 = x[1]
            h1 = x[2]

    rt = r1[AS]# route type of inputted AS
    if rt == 'c':
        print('Type of commercial route: customer')
    elif rt == 'r':
        print('Type of commercial route: peer')
    elif rt == 'p':
        print('Type of commercial route: provider')
    elif rt == None:
        print('Type of commercial route: unusable')
    print('Number of hops: ', h1[AS])
    '''
