import graphspace_utils, json_utils
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys



def getEdgeAttributes(edges):
    attrs = {} ## dictionary to return
    #weights = normalize(weights)
    for i in range(len(edges)):
        e = edges[i]
        source = e[0] ## set source node
        target = e[1] ## set target node
        if source not in attrs: ## initialize empty dict for source
            attrs[source] = {} ## (only if not seen yet)
        attrs[source][target] = {} ## init. (source,target) pair dict
    return attrs

def getNodeAttributes(nodes):
    attrs = {} ## dictionary to return
    for i in range(len(nodes)):
        n = nodes[i]
        attrs[n] = {} ## initialize empty dictionary for node n
        attrs[n]['id'] = n ## set the id (REQUIRED)
    return attrs

def graphit(name, dic):
    nodes = getNodes(dic)
    edges = getEdgesList(dic)
    #nodeFile = getNodeAttributes(nodes)
    nodeFile = None
    #edgeFile = getEdgeAttributes(edges)
    edgeFile = None
    data = json_utils.make_json_data(nodes, edges, nodeFile, edgeFile, name, 'Desc.', [''])
    jsonName = name + '.json'
    json_utils.write_json(data, jsonName)
    graphspace_utils.postGraph(name, jsonName, 'menzelk@reed.edu', 'sirstoat')
    #graphspace_utils.shareGraph(name,'menzelk@reed.edu','sirstoat','Lab7','aritz@reed.edu')

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

def getNodes(dic):
    nodes = []
    for i in dic:
        if not(i in nodes):
            nodes.append(i)
        for j in dic[i]:
            if not(j in nodes):
                nodes.append(j)
    return nodes

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

def getResidual(graph, flow):
    res = {}
    for i in graph:
        res[i] = {}
        for j in graph[i]:
            res[i][j] = graph[i][j] - flow[i][j]
    return res

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

def flowBetweenness(graph, social):
    nodes = getNodes(graph)
    scores = {}
    for i in nodes:
        scores[i] = {'inter':0, 'between':0, 'out':0}
    for i in range(len(nodes)):
        source = nodes[i]
        for j in range(i+1, len(nodes)):
            target = nodes[j]
            flows = fordFulkerson(graph, source, target)
            #print source, target
            #print
            nodeFlows = getNodeFlows(flows, nodes, source, target)
            for k in nodeFlows.keys():
                if k != nodes[i] and k != nodes[j]:
                    s_k = social[k]
                    s_i = social[nodes[i]]
                    s_j = social[nodes[j]]
                    print k, nodes[j], nodes[i]
                    print s_k, s_j, s_i
                    if s_k == s_j and s_j == s_i:
                        key = 'inter'
                    elif s_j == s_i:
                        key = 'out'
                    else:
                        key = 'between'
                    print key
                    print nodeFlows[k]
                    scores[k][key] = scores[k][key] + nodeFlows[k]
    return scores

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
    return path[target]

def sumAllMatrix(dic):
    edges = {}
    for i in dic:
        sm = 0
        for j in dic[i]:
            for k in dic[i][j]:
                sm += k
        edges[i] = sm
    return edges

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

def updateBetweeness(path, matrixes, edge, edges, graph):
    update = []
    for i in path:
        for j in path[i]:
            for k in path[i][j]:
                if edge in path:
                    update.append([i,j])
    for i in update:
        path[i[0]][i[1]] = dist(graph, i[0], i[1])
        for j in edges:
            count = 0
            for k in path[i[0]][i[1]]:
                if j in k:
                    count += 1
            matrixes[j][i[0]][i[1]] = float(count)/len(path[i[0]][i[1]])
    return

def GNmethod(graph):
    paths = {}
    tree = {}
    keys = graph.keys()
    edges = getEdgesList(graph, True)
    orderRemoved = []
    for i in range(len(keys)):
        paths[keys[i]] = {}
        for j in range(i+1, len(keys)):
            paths[keys[i]][keys[j]] = dist(graph, keys[i], keys[j])
            print keys[i], keys[j]
            for test in paths[keys[i]][keys[j]]:
                print test
    print 'Done with Paths'
    print
    sys.stdout.flush()
    matrixes = Betweeness(paths, edges)
    return  #I am here in my debugging, only one more left to do (Nice!)
    while len(edges) > 0:
        betweeness = sumAllMatrix(dic)
        score = 0
        edge = None
        for i in betweeness:
            if betweeness[i] > score:
                edge = i
        edges.remove(edge)
        orderRemoved.append(edge)
        listEdge = list(edge)
        graph[listEdge[0]].pop(listEdge[1])
        graph[listEdge[1]].pop(listEdge[0])
        updateBetweeness(paths, matrixes, edge, edges, graph)
    return orderRemoved


def main():
    #badgers, matrix = readIn()
    test = readInTest()

    path = depthFirstSearch(test, 'a', 'd')
    social = readSTest()
    flow = fordFulkerson(test, 'a', 'd')
    '''print 'Final'
    for i in flow:
        print i, flow[i]
    scores = flowBetweenness(test, social)
    for i in scores:
        for j in scores[i]:
            print i, j, scores[i][j]'''
    edgeOrder = GNmethod(test)
    '''inGroup = getPercentInGroup(badgers, matrix)
    groupSum = averageINGroups(badgers, inGroup, matrix)
    makeHistogram(inGroup, matrix, groupSum)
    '''







if __name__ == '__main__':
    main()
