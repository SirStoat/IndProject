
import graphspace_utils, json_utils, sys, utils


def readIn(filename):
    File = open(filename, 'r')
    data = File.read()
    File.close()

    data = data.split('\n')
    data.pop()

    dic = {}
    nodes = []
    for i in data:
        if filename == 'toy.txt':
            row = i.split('   ')
        else:
            row = i.split('\t')
        if not(row[0] in nodes):
            nodes.append(row[0])
        if not(row[1] in nodes):
            nodes.append(row[1])
        if row[0] in dic:
            dic[row[0]][row[1]] = float(row[2])
        else:
            dic[row[0]] = {row[1]:float(row[2])}
        if row[1] in dic:
            dic[row[1]][row[0]] = float(row[2])
        else:
            dic[row[1]] = {row[0]:float(row[2])}
    return dic, nodes

def dicTolists(graph):
    edges = []
    for i in graph:
        for j in graph[i]:
            if [i,j] in edges or [j,i] in edges:
                pass
            else:
                edges.append([i,j])
    return edges

def getNodeAttributes(nodes, clusters):
    attrs = {} ## dictionary to return
    colors = ['#ffff00', '#00ff00', '#0000ff']
    for i in range(len(nodes)):
        n = nodes[i]
        attrs[n] = {} ## initialize empty dictionary for node n
        attrs[n]['id'] = n ## set the id (REQUIRED)
        for i in range(len(clusters)):
            if n in clusters[i]:
                clusnum = i
        attrs[n]['background_color'] = colors[clusnum]
    return attrs

def graphit(name, nodes, edges, clusters):
    #nodeFile = getNodeAttributes(nodes, clusters)
    nodeFile = None
    edgeFile = None
    data = json_utils.make_json_data(nodes, edges, nodeFile, edgeFile, name, 'Desc.', [''])
    jsonName = name + '.json'
    json_utils.write_json(data, jsonName)
    graphspace_utils.postGraph(name, jsonName, 'menzelk@reed.edu', 'sirstoat')
    #graphspace_utils.shareGraph(name,'menzelk@reed.edu','sirstoat','Lab7','aritz@reed.edu')

def convertHighLow(graph):
    for i in graph:
        for j in graph[i]:
            graph[i][j] = 1-graph[i][j]
    return graph

def addtoQ(Q, thing, dist):
    i = 0
    added = False
    while i < len(Q):
        if dist[Q[i]] > dist[thing]:
            Q.insert(i, thing)
            added = True
            break
        i += 1
    if added == False:
        Q.append(thing)
    return Q

def dist(graph, start):
    Q = [start]
    dist = {Q[0]:0}
    while len(Q) > 0:
        node = Q.pop(0)
        neighbors = graph[node].keys()
        for i in neighbors:
            if not(i in dist) or dist[i] > dist[node] + graph[node][i]:
                dist[i] = dist[node] + graph[node][i]
                Q = addtoQ(Q, i, dist)
    dist.pop(start)
    return dist

def makeCompleat(graph, nodes):
    newGraph = {}
    for i in nodes:
        dists = dist(graph, i)
        newGraph[i] = {}
        for j in nodes:
            if i != j:
                newGraph[i][j] = dists[j]
    return newGraph

def getedgeWeights(graph):
    ls = []
    for i in graph:
        for j in graph[i]:
            ls.append(graph[i][j])
    ls.sort()
    ls = [ls[i] for i in range(0,len(ls), 2)]
    return ls

def bottleneck(graph, weight):
    newGraph = {}
    for i in graph:
        for j in graph[i]:
            if graph[i][j] <= weight:
                if i in newGraph:
                    newGraph[i][j] = graph[i][j]
                else:
                    newGraph[i] = {j:graph[i][j]}
    return newGraph

def squareGraph(graph):
    newGraph = {}
    for i in graph:
        for j in graph[i]:
            if i in newGraph:
                newGraph[i][j] = graph[i][j]
            else:
                newGraph[i] = {j:graph[i][j]}
            for k in graph[j]:
                if k != i:
                    newGraph[i][k] = graph[j][k]
    return newGraph

def getNodeDegree(graph, nodes):
    deg = {}
    for i in nodes:
        if i in graph:
            deg[i] = len(graph[i].keys())
        else:
            deg[i] = 0
    return deg

def getMIS(graph, nodesOld):
    deg = getNodeDegree(graph, nodesOld)
    nodes = nodesOld[:]
    ls = []
    while len(nodes) > 0:
        mn = 123456
        for i in nodes:
            if deg[i] < mn:
                mn = deg[i]
                node = i
        if node in graph:
            neighbors = graph[node].keys()
            connect = [i in ls for i in neighbors]
            if not(True in connect):
                ls.append(node)
        else:
            ls.append(node)
        nodes.pop(nodes.index(node))
    return ls

def getPartitions(graph, centers):
    partitions = [[] for i in centers]
    for i in graph:
        mn = 123456
        center = None
        for j in range(len(centers)):
            if i == centers[j]:
                mn = 0
                center = j
            elif mn > graph[i][centers[j]]:
                mn = graph[i][centers[j]]
                center = j
        partitions[center].append(i)
    return partitions

def bottleneck_k_centers(graph, nodes, k):
    edges = getedgeWeights(graph)
    i = 0.1
    stop = False
    while stop == False:
        #print int(i*10)+1, 'Times though', i, edges[len(edges)-1], i > edges[len(edges)-1]
        sys.stdout.flush()
        bottleGraph = bottleneck(graph, i)
        square = squareGraph(bottleGraph)
        MIS = getMIS(square, nodes)
        if len(MIS) <= k:
            stop = True
        i += 0.01
        #print len(MIS), 'centers'
    partitions = getPartitions(graph, MIS)
    return partitions, MIS

def avDist(graph, cluster, center):
    sm = 0
    tot = 0
    for i in range(len(center)):
        for j in cluster[i]:
            if j != center[i]:
                sm += graph[j][center[i]]
            tot += 1
    return float(sm)/tot

def main():
    graph, nodes = readIn('MI0059_gst_pull_down.txt')
    graph = utils.find_largest_cc(graph)
    i = 0
    while i < len(nodes):
        if not(nodes[i] in graph):
            nodes.pop(i)
        else:
            i += 1
    graph = convertHighLow(graph)
    comgraph = makeCompleat(graph, nodes)
    for i in range(5, 15):
        clusters, centers = bottleneck_k_centers(comgraph, nodes, i)
        print str(i) + '\t' + str(len(centers)) + '\t' + str(avDist(comgraph, clusters, centers))
#




if __name__ == '__main__':
    main()
