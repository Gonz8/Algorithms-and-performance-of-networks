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
        self.num_nodes = 0

    def getVertices(self):
        return self.adj.keys()

    def addVertex(self, vertex):
        self.adj[vertex] = []

    def getEdges(self, v):
        return self.adj[v]

    def addEdge(self, u, v, c):
        if u not in self.adj:
            self.addVertex(u)
            self.num_nodes += 1
        if v not in self.adj:
            self.addVertex(v)
            self.num_nodes += 1

        # Because the input file contains edges it is needed to create two links
        edge = Edge(u, v, c)
        self.adj[u].append(edge)
        edge_ = Edge(v, u, c)
        self.adj[v].append(edge_)
        edge.backedge= edge_
        edge_.backedge= edge

# Shortest path from a source node to a destination one algorithm using BFS method where the residual is taken into acount
def flowBFS(graph, source, destination):
    queue = [source] # Used as a FIFO queue
    seen = (source,) # Tuple of already visited nodes
    path = {} # Dictionary wich saves the path for each node
    path[source] = [] # Initialize the path for the source node as nothing

    while queue:
        current = queue.pop(0)
        if current == destination:
            return path[destination], None # means that still exists an augmenting path so no need to return the last reachable vertices (one part of the cut)
        for edge in graph.getEdges(current):
            residual = edge.capacity - edge.flow
            if residual > 0 and edge.sink not in seen:
                seen += (edge.sink,)
                path[edge.sink] = path[edge.source] + [edge]
                queue.append(edge.sink)
    return None, seen # no more augmenting paths so returns no path but a list of the last reachable vertices (one part of the cut)


# Edmonds Karp algorithm to find the max flow between a source and destination node
# Returns max flow plus the set of seen vertices when there is no augmenting path and the graph with the last modified flows in the edges
def edmondsKarp(graph, source, destination):
    path, seen = flowBFS(graph, source, destination)
    while path:
        residuals = [edge.capacity - edge.flow for edge in path]
        flow = min(residuals)
        for edge in path:
            edge.flow += flow
        path, seen = flowBFS(graph, source, destination)
    return sum(edge.flow for edge in graph.getEdges(source)), seen, graph


if __name__ == '__main__':
    import sys
    import copy

    Network = FlowNetwork()

    # Reads the text file and creates the network graph with capacities for each link = 1.
    f = open(str(sys.argv[1]),"r")
    for line in f:
        word = line.split()
        Network.addEdge(word[0], word[1], 1)

    f.closed

    # Creates a vector list with the minimum number of edges that separates one node from another from all vertices to all vertices
    min_connectivity = float("inf")
    for source in Network.getVertices():
        for destination in Network.getVertices():
            if source == destination:
                continue
            aux_min, aux_reachable, aux_graph = edmondsKarp(copy.deepcopy(Network), source, destination)
            if aux_min < min_connectivity: # the min conectivity is the minimum between all the pairs of nodes in the graph, saves also the list of last reachable nodes (one part of the cut) and the graph with the most recent flow informations
                min_connectivity = aux_min
                reachable_vertices = aux_reachable
                flow_graph = aux_graph
                s = source
                d = destination

    # For each vertex in one side of the cut check if has edges that have a saturated flow, this means that is an edge that separates both cuts
    #print(s,d)
    #print(reachable_vertices)
    print('The minimum number of edges needed to cut the graph in two are ', min_connectivity,'.')
    for vertex in reachable_vertices:
        for edge in flow_graph.getEdges(vertex):
            if edge.flow > 0 and edge.sink not in reachable_vertices:
                print(edge.source, '--', edge.sink, edge.flow)
