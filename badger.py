import graphspace_utils, json_utils
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt



def getEdgeAttributes(edges):
    attrs = {} ## dictionary to return
    #weights = normalize(weights)
    print weights
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

    print data
    data = data.split('\n')
    head = data.pop(0)
    head = head.split('\t')
    head.pop(0)
    data.pop()
    dic = {}
    print head
    for i in range(len(data)):
        row = data[i].split('\t')
        print row
        tail = row.pop(0)
        dic[head[i]] = {}
        for j in range(len(row)):
            num = int(row[j])
            if num > 0:
                dic[head[i]][head[j]] = num
    return dic

def getEdgesList(dic):
    edges = []
    for i in dic:
        for j in dic[i]:
            if not([i,j] in edges) and not([j,i] in edges):
                edges.append([i,j])
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
    for i in badgers:
        print i, info[i]['Social Group']
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
    print path
    while path[len(path)-1] != target and len(disc) < nodes:
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
        else:
            path.pop()
    if path[len(path)-1] != target:
        return None
    else:
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
            flow[i][j] = graph[i][j]
    res = getResidual(graph , flow)
    path = depthFirstSearch(graph, source, target)
    while path != None:


def main():
    #badgers, matrix = readIn()
    test = readInTest()
    print 'Start Test'
    for i in test:
        print i, test[i]

    print
    path = depthFirstSearch(test, 'a', 'd')
    print path

    #graphit('test', test)
    '''inGroup = getPercentInGroup(badgers, matrix)
    groupSum = averageINGroups(badgers, inGroup, matrix)
    makeHistogram(inGroup, matrix, groupSum)
    '''







if __name__ == '__main__':
    main()
