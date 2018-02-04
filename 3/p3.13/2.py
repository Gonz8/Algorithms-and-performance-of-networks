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
        residuals = [edge.capacity - edge.flow for edge in path]
        flow = min(residuals)
        for edge in path:
            edge.flow += flow
        path = flowBFS(graph, source, destination)
    return sum(edge.flow for edge in graph.getEdges(source))


if __name__ == '__main__':
    import sys
    import time as t
    import matplotlib.pyplot as plt
    import copy

    Network = FlowNetwork()

    # Reads the text file and creates the network graph with capacities for each link = 1.
    f = open(str(sys.argv[1]),"r")
    for line in f:
        word = line.split()
        Network.addEdge(word[0], word[1], 1)

    f.closed

    # Creates a vector list with the minimum number of edges that separates one node from another from all vertices to all vertices
    total_counts = 0
    connectivity_list = []
    for source in Network.getVertices():
        for destination in Network.getVertices():
            if source == destination:
                continue
            connectivity_list.append(edmondsKarp(copy.deepcopy(Network), source, destination))
            total_counts += 1 # number of runs of Edonds Karp algorithm

    # Process the list so it cn be plotted as a complementary cumulative distribution of the minimum number of edges that separates one node from another
    _max = max(connectivity_list) # maximum number of edges to be disconected
    min_connect = [0] * (_max + 2)
    for x in connectivity_list:
        min_connect[x] += 1

    for x in range(_max - 1, 0, -1):
        min_connect[x] += min_connect[x+1]

    for x in range(len(min_connect)):
        min_connect[x] = min_connect[x] / total_counts

    plt.plot(list(range(1, _max + 2)), min_connect[1:])
    plt.title('Complementary cumulative distribution of the minimum number of edges that separates one node from another')
    plt.ylabel('Pairs of nodes')
    plt.xlabel('k edges')
    plt.show()
