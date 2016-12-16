from badger import *
import math
import hw5


def getEdgeAttributes(edges, graph, name):
    attrs = {} ## dictionary to return
    #weights = normalize(weights)
    for i in range(len(edges)):
        e = edges[i]
        source = e[0] ## set source node
        target = e[1] ## set target node
        if source not in attrs: ## initialize empty dict for source
            attrs[source] = {} ## (only if not seen yet)
        attrs[source][target] = {} ## init. (source,target) pair dict
        #print math.log(graph[source][target]*1000)
        if 'raw' in name:
            var = 2
        else:
            var = 1
        print math.log(normalizeDicDic(graph)[source][target]*10000000, 10)
        attrs[source][target]['width'] = math.log(normalizeDicDic(graph)[source][target]*100000, 10)/2
    return attrs

def getNodeAttributes(nodes, demo, status):
    attrs = {} ## dictionary to return
    color = ['#ffff00', '#00ff00', '#ff0000', '#0000ff', '#00ffff', '#ff00ff', '#000000', '#ff0066']
    number = [str(i) for i in range(1,9)]
    color = dict(zip(number, color))
    for i in range(len(nodes)):
        n = nodes[i]
        attrs[n] = {} ## initialize empty dictionary for node n
        attrs[n]['id'] = n ## set the id (REQUIRED)
        attrs[n]['background_color'] = color[demo[n]['Social Group']]
        if demo[n]['Social Group'] == '7':
            attrs[n]['color'] = '#ffffff'
        infect = demo[n]['Infection Status']
        if infect == 'P':
            attrs[n]['border_color'] = '#ff0000'
        else:
            attrs[n]['border_color'] = '#00ff00'
        attrs[n]['border_width'] = 2
        #attrs[n]['border_style'] = ['dotted']
        size = math.log(normalizeDic(status['between'])[n]*1000)*10
        attrs[n]['height'] = size
        attrs[n]['width'] = size
        attrs[n]['popup'] = 'Size is:\t' + str(size) + '\nGroup is:\t' + demo[n]['Social Group'] + '\nInfection Status:\t' + demo[n]['Infection Status']
    return attrs

def graphit(name, dic, badgers):
    nodes = getNodes(dic)
    edges = getEdgesList(dic)
    if 'k-means' in name:
        clusters, centers = hw5.bottleneck_k_centers(compleatGraph(dic), nodes, 8)
        edges = cutExtranious(clusters)
    status = readInNodeFlows()
    nodeFile = getNodeAttributes(nodes, badgers, status)
    #nodeFile = None
    edgeFile = getEdgeAttributes(edges, dic, name)
    #edgeFile = None
    data = json_utils.make_json_data(nodes, edges, nodeFile, edgeFile, name, 'Desc.', [''])
    jsonName = name + '.json'
    json_utils.write_json(data, jsonName)
    graphspace_utils.postGraph(name, jsonName, 'menzelk@reed.edu', 'sirstoat')
    #graphspace_utils.shareGraph(name,'menzelk@reed.edu','sirstoat','Lab7','aritz@reed.edu')

def GNgroupsToDic(groups):
    dic = {}
    for i in range(len(groups)):
        for j in groups[i]:
            dic[j] = {}
            dic[j]['Social Group'] = str(i+1)
    return dic

def compleatGraph(graph):
    for i in graph:
        for j in graph[i]:
            if not(j in graph):
                graph[j] = {i:graph[i][j]}
            elif not(i in graph[j]):
                graph[j][i] = graph[i][j]
    return graph

def cutExtranious(edges, groups):
    dic = GNgroupsToDic(groups)
    for i in range(len(edges)):
        if dic[edges[i][0]] != dic[edges[i][1]]:
            edges.pop(i)
    return edges

def main():
    badgers, matrix = readIn()
    '''graphs = [ 'GN-flow-list', 'NG-raw_list']
    #'NG-raw_list'
    for i in graphs:
        if 'raw' in i:
            name = 'raw'
            data = matrix
        else:
            name = 'flow'
            data = readInEdgeFlows()
        graphit(name + '-bace-New', data, badgers)
        edges = readInEdges(i)
        for i in range(8, 10):
            groups, groupedGraph = GNGroups(edges, data, i)
            dic = GNgroupsToDic(groups)
            graphit(name + '-groups-' + str(i), groupedGraph, badgers)'''
    graphit('testStatus1', readInEdgeFlows(), badgers)
    graphit('testStatus2', matrix, badgers)







if __name__ == '__main__':
    main()
