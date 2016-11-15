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

def graphit(name, nodes, edges):
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

def getEdgesList(dic):
    edges = []
    for i in dic:
        for j in dic[i]:
            if not([i,j] in edges) and not([j,i] in edges):
                edges.append([i,j])
    return edges

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

def makeHistogram(inGroup, matrix):
    pIG = []
    for i in inGroup:
        pIG.append(inGroup[i])
    nn = []
    for i in inGroup:
        nn.append(len(matrix[i].keys()))
    plt.plot(nn, pIG, 'or')
    plt.xlabel('Number of neighbors')
    plt.ylabel('Percent of neighbors in social group')
    print 'Badger ID | Number of Neighbors | Percent Edges in social group'
    for i in inGroup:
        nn = len(matrix[i].keys())
        print i,'|', nn,'|', inGroup[i]
    #plt.show()

def main():
    badgers, matrix = readIn()
    '''print len(badgers)
    for i in badgers:
        print i, badgers[i]
    print matrix['008p']['012b']
    edges = getEdgesList(matrix)
    #graphit('badgers_Test', badgers.keys(), edges)

    #group5 = getSubgraph(badgers, ['5', '4'], matrix)
    #graphit('group_5', group5.keys(), getEdgesList(group5))'''

    inGroup = getPercentInGroup(badgers, matrix)

    makeHistogram(inGroup, matrix)








if __name__ == '__main__':
    main()
