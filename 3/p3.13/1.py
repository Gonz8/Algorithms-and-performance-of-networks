class Edge(object):
    def __init__(self, u, v, c):
        self.source = u
        self.sink = v
        self.capacity = c
        self.flow = 0

    def __str__(self):
        return 'From ' + str(self.source) + ' to ' + str(self.sink)

class FlowNetwork(object):
    def __init__(self):
        self.adj = {}

    def getVertices(self):
        return self.adj.keys()

    def addVertex(self, vertex):
        self.adj[vertex] = []

    def getEdges(self, v):
        return self.adj[v]

    def addEdge(self, u, v, c):
        if u not in self.adj:
            self.addVertex(u)
        if v not in self.adj:
            self.addVertex(v)

        # Because the input file contains edges it is needed to create two links
        edge = Edge(u, v, c)
        self.adj[u].append(edge)
        edge_ = Edge(v, u, c)
        self.adj[v].append(edge_)

# Shortest path from a source node to a destination one algorithm using BFS method where the residual is taken into acount
def flowBFS(graph, source, destination):
    queue = [source] # Used as a FIFO queue
    seen = (source,) # Tuple of already visited nodes
    path = {} # Dictionary wich saves the path for each node
    path[source] = [] # Initialize the path for the source node as nothing
    while queue:
        current = queue.pop(0)
        if current == destination:
            return path[destination]
        for edge in graph.getEdges(current):
            residual = edge.capacity - edge.flow
            if residual > 0 and edge.sink not in seen:
                seen += (edge.sink,)
                path[edge.sink] = path[edge.source] + [edge]
                queue.append(edge.sink)

# Edmonds Karp algorithm to find the max flow between a source and destination node
def edmondsKarp(graph, source, destination):
    path = flowBFS(graph, source, destination)
    while path:
        for edge in path:
            edge.flow += 1
        path = flowBFS(graph, source, destination)
    return sum(edge.flow for edge in graph.getEdges(source))

if __name__ == '__main__':
    import sys
    import time as t

    Network = FlowNetwork()

    # Reads the text file and creates the network graph with capacities for each link = 1.
    f = open(str(sys.argv[1]),"r")
    for line in f:
        word = line.split()
        Network.addEdge(word[0], word[1], 1)

    f.closed

    # Asks user for source id
    while True:
        source = input("\nInput a source id: ")
        if source not in tuple(Network.getVertices()):
            print("Not a valid source.\n")
        else:
            break
    # Asks user for destination id
    while True:
        destination = input("Input a destination id: ")
        if destination not in tuple(Network.getVertices()) or destination == source:
            print("Not a valid destination.\n")
        else:
            break

    # Calculates the max flow wich corresponds to the minimum number of edges to be removed so both nodes are separated in the graph
    edge_connectivity = edmondsKarp(Network, source, destination)
    print('Result:', edge_connectivity)
