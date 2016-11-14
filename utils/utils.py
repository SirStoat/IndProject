
import random

##
#Input: a file name (string)
#Output: a dictionary such that keys are tails of edges and values are dictionaries
#such that keys and tails of edges and values are dictionaries such that the keys
#is attribute name and value is the value of the attribute
#assumes directed graphs
def readIn(filename):
    File = open(filename, 'r')
    data = File.read()
    File.close()
    data = data.split('\n')
    header = data.pop(0)
    data.pop()
    header = header.split(',')
    dic = {}
    for i in range(len(data)):
        row = data[i].split(',')
        if row[0] in dic:
            if not(row[1] in dic[row[0]].keys()):
                dic[row[0]][row[1]] = {}
            if len(header) > 2:
                for j in range(2,len(header)):
                    dic[row[0]][row[1]][header[j]] = row[2]
        else:
            dic[row[0]] = {row[1]:{}}
            if len(header) > 2:
                    for j in range(2,len(header)):
                        dic[row[0]][row[1]][header[j]] = row[2]
    return dic

##
#Input: graph of format described in readIn, boolean to indicate directed
#Output: A list of nodes and a list of edges which are two element lists.
def graphToLists(graph, direc = False):
    nodes = []
    edges = []
    for i in graph:
        if not(i in nodes):
            nodes.append(i)
        for j in graph[i]:
            if not(j in nodes):
                nodes.append(j)
            if not([i,j] in edges) or (direc and not([j,i] in edges)):
                edges.append([i,j])
    return nodes, edges

##
#Input: graph of format described in readIn
#Output: a dictionary such that keys are nodes and values are lists of neighbors
#assumes undirected graph
def graphToAdjList(graph):
    dic = {}
    for i in graph:
        for j in graph[i]:
            if i in dic:
                if not(j in dic[i]):
                    dic[i].append(j)
            else :
                dic[i] = [j]

            if j in dic:
                if not(i in dic[j]):
                    dic[j].append(i)
            else :
                dic[j] = [i]
    return dic

##
#Input: graph of format described in readIn and optional input for starting node
#Output: a list of nodes that are all connected to the starting node.
def BFS(graph, s = None):
    graph = graphToAdjList(graph)
    if s == None:
        s = graph.keys()[0]
    visited = [s]
    Q = [s]
    while len(Q) > 0:
        w = Q.pop()
        neighbors = graph[w]
        for i in neighbors:
            if not(i in visited):
                visited.append(i)
                Q.append(i)
    return visited

#Input: graph of format described in readIn
#OUtput: a graph of format described in readIn that is the largest connected
#component of the input graph
def find_largest_cc(graph):
    nodes, edges = graphToLists(graph)
    nodes = nodes
    largest = 0
    conComp = []
    while len(nodes) > 0:
        temp = BFS(graph, nodes[0])
        if largest < len(temp):
            largest = len(temp)
            conComp = temp
        for i in temp:
            nodes.remove(i)
    out = {}
    for i in conComp:
        if i in graph:
            out[i] = graph[i]
    return out

##
#Input: graph of format described in readIn and option for seeding
#Output: a random node (normally as string)
def getRanEdge(graph, seed = False):
    if seed:
        random.seed(5311995)
    tail = random.choice(graph.keys())
    head = random.choice(graph[tail].keys())
    return [tail,head]

##
#Input: graph of format described in readIn and option for seeding
#Output: an random edge (normally as a list of two elements which are nodes)
def getRanNode(graph, seed = False):
    if seed == True:
        random.seed(5311995)
    nodes = []
    for i in graph:
        if not(i in nodes):
            nodes.append(i)
        for j in graph[i]:
            if not(j in nodes):
                nodes.append(j)
    return random.choice(nodes)


def rgb_to_hex(red, green, blue):
    MHV = 255
    r = int(red*MHV)
    g = int(green*MHV)
    b = int(blue*MHV)
    out = '#{:02x}{:02x}{:02x}'.format(r,g,b)
    return out
