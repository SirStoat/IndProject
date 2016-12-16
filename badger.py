import graphspace_utils, json_utils
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys
##
#This reads in the the badger matrix file (BadgerMatrix.txt) and the badger info file
#(BadgerInfo.txt) and creates a data object for the matrix and the info
#Matrix: dictionary of dictionaries key1 source, key2 target, value: weight
#Info: key1 badger, key2 type of info, value: value
def readIn():
    File = open('BadgerMatrix.txt')
    matrix = File.read()
    File.close()
    File = open('BadgerInfo.txt')
    info = File.read()
    File.close()

    info = info.split('\n')
    head = info.pop(0)
    head = head.split('\t')
    info.pop()
    badgerDemo = {}
    for i in info:
        row = i.split('\t')
        badgerDemo[row[0]] = {head[1]:row[1], head[2]:row[2], head[3]:row[3]}

    matrix = matrix.split('\n')
    badgers = matrix.pop(0)
    badgers = badgers.split('\t')
    badgers.pop(0)
    network = {}
    for i in range(len(matrix)):
        row = matrix[i].split('\t')
        badger = row.pop(0)
        network[badger] = {}
        for j in range(len(badgers)):
            row[j] = int(row[j])
            if row[j] > 0:
                network[badger][badgers[j]] = row[j]
    return badgerDemo, network

##
#reads in the toy matrix
#same as normal read in
def readInTest():
    File = open('test.txt', 'r')
    data = File.read()
    File.close()

    data = data.split('\n')
    head = data.pop(0)
    head = head.split('\t')
    head.pop(0)
    data.pop()
    dic = {}
    for i in range(len(data)):
        row = data[i].split('\t')
        tail = row.pop(0)
        dic[head[i]] = {}
        for j in range(len(row)):
            num = int(row[j])
            if num > 0:
                dic[head[i]][head[j]] = num
    return dic

##
#input: graph in dic of dic format
#output: list of edges: in either list or frozenset format
def getEdgesList(dic, isSet=False):
    edges = []
    for i in dic:
        for j in dic[i]:
            if isSet == False:
                if not([i,j] in edges) and not([j,i] in edges):
                    edges.append([i,j])
            elif isSet == True:
                if not(frozenset([i,j]) in edges):
                    edges.append(frozenset([i,j]))
    return edges

##
#input: graph in form of dic of dics
#output: list of nodes
def getNodes(dic):
    nodes = []
    for i in dic:
        if not(i in nodes):
            nodes.append(i)
        for j in dic[i]:
            if not(j in nodes):
                nodes.append(j)
    return nodes

##
#test function, no longer needed
def getSubgraph(info, groups, matrix):
    subgraph = {}
    badgers = []
    for i in info:
        if info[i]['Social Group'] in groups:
            badgers.append(i)
    for i in matrix:
        for j in matrix[i]:
            if i in badgers and j in badgers:
                if not(i in subgraph):
                    subgraph[i] = {j:matrix[i][j]}
                else:
                    subgraph[i][j] = matrix[i][j]
    return subgraph

##
#test function, i don't know why i have it now
def getPercentInGroup(info, matrix):
    out = {}
    for i in matrix:
        igroup = info[i]['Social Group']
        inGroup = 0
        for j in matrix[i]:
            jgroup = info[j]['Social Group']
            if igroup == jgroup:
                inGroup += 1
        out[i] = float(inGroup)/len(matrix[i].keys())
    return out

##
#visualizing stuff
def makeHistogram(inGroup, matrix, groupSum):
    pIG = []
    for i in inGroup:
        pIG.append(inGroup[i])
    nn = []
    for i in inGroup:
        nn.append(len(matrix[i].keys()))
    plt.plot(nn, pIG, 'or')
    plt.xlabel('Number of neighbors')
    plt.ylabel('Percent of neighbors in social group')
    print 'Group & Proportion of Internal Edges & Number Edges'
    print '\\hline'
    for i in groupSum:
        print i,'&', (groupSum[i]['number']/2),'&', groupSum[i]['Percent']/(groupSum[i]['number']/2), '\\\\'
        print '\\hline'
    plt.savefig('writeup/proportionInOut.png')

##
#visualizing stuff
def averageINGroups(info, inGroup, matrix):
    groups = {}
    for i in info:
        group = info[i]['Social Group']
        if group in groups:
            groups[group]['Percent'] = groups[group]['Percent'] + inGroup[i]*len(matrix[i].keys())
            groups[group]['number'] = groups[group]['number'] + len(matrix[i].keys())
        else:
            groups[group] = {'Percent':inGroup[i]*len(matrix[i].keys()), 'number':len(matrix[i].keys())}
    return groups

##
#input: start, end, dictionary
#output: a path using depth first search
def depthFirstSearch(dic, start, target):
    nodes = getNodes(dic)
    disc = [start]
    path = [start]
    while len(path) > 0 and path[len(path)-1] != target :
        current = path[len(path)-1]
        if current in dic:
            neighbors = dic[start]
            nxt = None
            score = 0
            for i in dic[current]:
                if not(i in disc) and dic[current][i] > score:
                    score = dic[current][i]
                    nxt = i
            if nxt == None:
                path.pop()
            else:
                path.append(nxt)
                disc.append(nxt)
    return path

##
#Helper for fordfulkerson subtracts vales of two graphs from each other
def getResidual(graph, flow):
    res = {}
    for i in graph:
        res[i] = {}
        for j in graph[i]:
            res[i][j] = graph[i][j] - flow[i][j]
    return res

##
#Helper for flowBetweenness
#using fordFulkerson method to find flows on graph givin start and end
def fordFulkerson(graph, source, target):
    flow = {}
    #initiate flow graph
    for i in graph:
        flow[i] = {}
        for j in graph[i]:
            flow[i][j] = 0
    res = getResidual(graph , flow)
    path = depthFirstSearch(res, source, target)
    count = 0
    while len(path) > 0:
        score = 100
        for i in range(len(path)-1):
            current = path[i]
            nxt = path[i+1]
            if res[current][nxt] < score:
                score = res[current][nxt]
        for i in range(len(path)-1):
            current = path[i]
            nxt = path[i+1]
            flow[current][nxt] = flow[current][nxt] + score
            flow[nxt][current] = flow[nxt][current] - score
        res = getResidual(graph, flow)
        path = depthFirstSearch(res, source, target)
    return flow

##
#helper for flowBetweeness
#adds up flows from edges gotten by fordFulkerson
def getNodeFlows(flows, nodes, source, target):
    dic = {}
    total = 0
    for i in flows[source]:
        total += flows[source][i]
    for i in flows:
        score = 0
        for j in flows[i]:
            score += abs(flows[i][j])
        if i != source and i != target:
            score = float(score)/(2*total)
        dic[i] = score
    return dic

##
#makes sure edge flows are posative
def getedgeFlows(flows):
    for i in flows:
        for j in flows[i]:
            flows[i][j] = abs(flows[i][j])
    return flows

##
#Input: graph, social info, and whether you want node or edge flows
#output:Nodes: three dicitonaries for flow betweenness between groups
#               within groups and inter groups
#       Edges: one dic dic of a graph with edge weight as flowBetweenness
def flowBetweenness(graph, social, placement = 'node'):
    nodes = getNodes(graph)
    scores = {}
    edgeFlows = {}
    for i in graph:
        edgeFlows[i] = {}
        for j in graph[i]:
            edgeFlows[i][j] = 0
    for i in nodes:
        scores[i] = {'inter':0, 'between':0, 'out':0}
    for i in range(len(nodes)):
        source = nodes[i]
        sys.stdout.flush()
        for j in range(i+1, len(nodes)):
            print 'Finding Flow for nodes:', nodes[i], nodes[j]
            sys.stdout.flush()
            target = nodes[j]
            flows = fordFulkerson(graph, source, target)
            if placement == 'node':
                nodeFlows = getNodeFlows(flows, nodes, source, target)
                for k in nodeFlows.keys():
                    if k != nodes[i] and k != nodes[j]:
                        s_k = social[k]
                        s_i = social[nodes[i]]
                        s_j = social[nodes[j]]
                        if s_k == s_j and s_j == s_i:
                            key = 'inter'
                        elif s_j == s_i:
                            key = 'out'
                        else:
                            key = 'between'
                        scores[k][key] = scores[k][key] + nodeFlows[k]
            elif placement == 'edge':
                getedgeFlows(flows)
                neighbors = flows[nodes[i]]
                totFlow = 0
                for n in neighbors:
                    totFlow += flows[nodes[i]][n]
                totFlow = float(totFlow)
                for k in flows:
                    for l in flows[k]:
                        edgeFlows[k][l] = edgeFlows[k][l] + flows[k][l]/totFlow
    if placement == 'node':
        return scores
    elif placement == 'edge':
        return edgeFlows

##
#Reads in a social groups for toy graph
def readSTest():
    File = open('testS.txt')
    data = File.read()
    File.close()
    data = data.split('\n')
    data.pop()
    dic = {}
    for i in data:
        row = i.split('\t')
        dic[row[0]] = row[1]
    return dic

##
#helper function for GNmethod, helps make paths
def addPaths(path, old, new, action):
    if action == 'replace':
        oldPath = path[old]
        newPath = [[] for i in range(len(oldPath))]
        for i in range(len(oldPath)):
            newPath[i] = oldPath[i] + [frozenset([old, new])]
        path[new] = newPath
    elif action == 'add':
        oldPath = path[old]
        newPath = [[] for i in range(len(oldPath))]
        for i in range(len(oldPath)):
            newPath[i] = oldPath[i] + [frozenset([old, new])]
        path[new] = path[new] + newPath

##
#Helper function for dist
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

##
#helper function for GNmethod
#finds shortest paths
def dist(graph, start, target):
    Q = [start]
    dist = {Q[0]:0}
    path = {start:[[]]}
    while len(Q) > 0:
        node = Q.pop(0)
        neighbors = graph[node].keys()
        for i in neighbors:
            if not(i in dist) or dist[i] > dist[node] + graph[node][i]:
                dist[i] = dist[node] + graph[node][i]
                Q = addtoQ(Q, i, dist)
                addPaths(path, node, i, 'replace')
            elif not(i in dist) or dist[i] == dist[node] + graph[node][i]:
                addPaths(path, node, i, 'add')
    if target in path:
        return path[target]
    else:
        return []

##
#Helper for GNmethod
#sums paths for betweennes score
def sumAllMatrix(dic):
    edges = {}
    for i in dic:
        sm = 0
        for j in dic[i]:
            for k in dic[i][j]:
                sm += dic[i][j][k]
        edges[i] = sm
    return edges

##
#helper for GNmethod
#helps with Betweeness score
def Betweeness(paths, edges):
    dic = {}
    for i in edges:
        matrix = {}
        for j in paths:
            matrix[j] = {}
            for k in paths[j]:
                count = 0
                for l in paths[j][k]:
                    if i in l:
                        count += 1
                matrix[j][k] = float(count)/len(paths[j][k])
        dic[i] = matrix
    return dic

##
#helper for GNmehtod
#updates betweennes scores after edge removel
def updateBetweeness(paths, matrixes, edge, edges, graph):
    update = []
    for i in paths:
        for j in paths[i]:
            for k in paths[i][j]:
                #print edge
                #print k
                if edge in k:
                    update.append([i,j])
    for i in update:
        temp = dist(graph, i[0], i[1])
        paths[i[0]][i[1]] = temp
        for j in edges:
            count = 0
            for k in paths[i[0]][i[1]]:
                if j in k:
                    count += 1
            if len(paths[i[0]][i[1]]) != 0:
                matrixes[j][i[0]][i[1]] = float(count)/len(paths[i[0]][i[1]])
            else:
                matrixes[j][i[0]][i[1]] = 0
    return

##
#Input: a graph
#output: a list of edges (list)
#edges are in the order that they were removed in GNmethod
def GNmethod(graph):
    paths = {}
    tree = {}
    keys = graph.keys()
    dic = {}
    for i in graph:
        dic[i] = {}
        for j in graph[i]:
            dic[i][j] = graph[i][j]
    graph = dic
    edges = getEdgesList(graph, True)
    orderRemoved = []
    for i in range(len(keys)):
        paths[keys[i]] = {}
        for j in range(i+1, len(keys)):
            paths[keys[i]][keys[j]] = dist(graph, keys[i], keys[j])
    matrixes = Betweeness(paths, edges)
    while len(edges) > 0:
        betweeness = sumAllMatrix(matrixes)
        score = 0
        edge = None
        for i in betweeness:
            if betweeness[i] > score:
                edge = i
                score = betweeness[i]
        edges.remove(edge)
        orderRemoved.append(edge)
        listEdge = list(edge)
        graph[listEdge[0]].pop(listEdge[1])
        graph[listEdge[1]].pop(listEdge[0])
        matrixes.pop(edge)
        updateBetweeness(paths, matrixes, edge, edges, graph)
    return orderRemoved

##
#helper for getAllCCs
#takes graph and starting point
#gives a connected component: lists of nodes
def getCC(graph, start):
    Q = [start]
    cc = [start]
    while len(Q) > 0:
        sys.stdout.flush()
        node = Q.pop(0)
        neighbors = graph[node].keys()
        for i in neighbors:
            if not(i in cc):
                cc.append(i)
                Q.append(i)
    return cc

##
#helper for GNGroups
#input: a graph
#output: list of all connected components
def getAllCCs(graph):
    nodes = getNodes(graph)
    allCCs = []
    while len(nodes) > 0:
        ccc = getCC(graph, nodes[0])
        allCCs.append(ccc)
        for i in ccc:
            nodes.remove(i)
    return allCCs

##
#Gets output from GNMethod (edges) and a graph and number of groups
#output is a list of groupss of the number inputed
def GNGroups(edges, graph, number):
    edges = edges[:]
    groups = []
    dic = {}
    for i in graph:
        dic[i] = {}
        for j in graph[i]:
            dic[i][j] = graph[i][j]
    graph = dic
    while len(groups) < number and len(edges) > 0:
        sys.stdout.flush()
        edge = edges.pop(0)
        outKey = graph.keys()
        for i in outKey:
            inKey = graph[i].keys()
            for j in inKey:
                if edge == frozenset([i,j]):
                    graph[i].pop(j)
        groups = getAllCCs(graph)
    return groups, graph

##
#Writes output from node flowBetweenness
def writeEdgeFlows():
    badger, matrix = readIn()
    #matrix = readInTest()
    #badger = readSTest()
    print 'read in matrix'
    sys.stdout.flush()
    scores = flowBetweenness(matrix, badger, 'edge')
    print 'got flow scores'
    sys.stdout.flush()
    File = open('edgeFlow.txt', 'w')
    for i in scores:
        for j in scores[i]:
            File.write(i + "\t" + j + '\t' + str(scores[i][j]))
            File.write('\n')
    File.close()
    return

##
#writes output from GNmethod
def writeNGresults():
    badger, matrix = readIn()
    #matrix = readInTest()
    #badger = readSTest()
    flows = readInEdgeFlows()
    raw = GNmethod(matrix)
    File = open('GN-raw-list.txt', 'w')
    for i in raw:
        edge = list(i)
        File.write(edge[0] + '\t' + edge[1] + '\n')
    File.close()
    flowB = GNmethod(flows)
    File = open('GN-flow-list.txt', 'w')
    for i in flowB:
        edge = list(i)
        File.write(edge[0] + '\t' + edge[1] + '\n')
    File.close()
    return

##
#reads in output of writeEdgeFlows
def readInEdgeFlows():
    File = open('edgeFlow.txt', 'r')
    data = File.read()
    File.close()
    data = data.split('\n')
    data.pop()
    dic = {}
    for i in data:
        row = i.split('\t')
        if row[0] in dic:
            dic[row[0]][row[1]] = float(row[2])
        else:
            dic[row[0]] = {row[1]:float(row[2])}
        if row[01] in dic:
            dic[row[1]][row[0]] = float(row[2])
        else:
            dic[row[1]] = {row[0]:float(row[2])}
    return dic

##
#reads in output of writeNodeVals
def readInNodeFlows():
    File = open('nodeFlows.txt', 'r')
    data = File.read()
    File.close()
    data = data.split('\n')
    data.pop()
    demo = {}
    head = data.pop(0)
    head = head.split('\t')
    for i in range(1, len(head)):
        demo[head[i]] = {}
        for j in data:
            row = j.split('\t')
            demo[head[i]][row[0]] = float(row[i])
    return demo

##
#reads in output of writeEdgeFlows
def writeNodeVals():
    badger, matrix = readIn()
    #matrix = readInTest()
    #badger = readSTest()
    scores = flowBetweenness(matrix, badger, 'node')
    File = open('nodeFlows.txt', 'w')
    key = scores[scores.keys()[0]].keys()
    File.write('Bader')
    for i in key:
        File.write('\t' + i)
    File.write('\n')
    for i in scores:
        File.write(i)
        for j in key:
            File.write('\t' + str(scores[i][j]))
        File.write('\n')
    return

##
#normalizes dicitonaries
def normalizeDic(dic):
    high = 0
    for i in dic:
        if dic[i] > high:
            high = dic[i]
    for i in dic:
        dic[i] = float(dic[i])/high
    return dic

##
#mamalizes dictionaris of dicitonaries
def normalizeDicDic(dic):
    high = 0
    for i in dic:
        for j in dic[i]:
            if dic[i][j] > high:
                high = dic[i][j]
    for i in dic:
        for j in dic[i]:
            dic[i][j] = float(dic[i][j])/high
    return dic

##
#reads in output of writeNGresults
def readInEdges(name):
    File = open(name, 'r')
    data = File.read()
    File.close()

    data = data.split('\n')
    data.pop()
    edges = []
    for i in data:
        edge = i.split('\t')
        edges.append(frozenset(edge))
    return edges


def main():
    '''badgers, matrix = readIn()
    test = readInTest()

    path = depthFirstSearch(test, 'a', 'd')
    social = readSTest()
    flow = fordFulkerson(test, 'a', 'd')
    print 'Final'
    for i in flow:
        print i, flow[i]
    scores = flowBetweenness(test, social, 'edge')
    for i in scores:
        for j in scores[i]:
            print i, j, scores[i][j]'''
    '''edgeOrder = GNmethod(test)
    print 'done with part 1'
    sys.stdout.flush()
    groups = GNGroups(edgeOrder, test, 10)
    for i in groups:
        print i
    print edgeOrder'''
    '''inGroup = getPercentInGroup(badgers, matrix)
    groupSum = averageINGroups(badgers, inGroup, matrix)
    makeHistogram(inGroup, matrix, groupSum)
    '''
    #writeEdgeFlows()
    #writeNodeVals()
    #writeNGresults()
    '''edges = readInEdges('GN-raw-list')
    for i in edges:
        print i'''
