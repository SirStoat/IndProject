from badger import *
import math


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
        size = math.log(normalizeDic(status['between'])[n]*1000)*7
        attrs[n]['height'] = size
        attrs[n]['width'] = size
        attrs[n]['popup'] = 'Size is:\t' + str(size) + '\nGroup is:\t' + demo[n]['Social Group'] + '\nInfection Status:\t' + demo[n]['Infection Status']
    return attrs

def graphit(name, dic, badgers):
    nodes = getNodes(dic)
    edges = getEdgesList(dic)
    status = readInNodeFlows()
    nodeFile = getNodeAttributes(nodes, badgers, status)
    #nodeFile = None
    #edgeFile = getEdgeAttributes(edges)
    edgeFile = None
    data = json_utils.make_json_data(nodes, edges, nodeFile, edgeFile, name, 'Desc.', [''])
    jsonName = name + '.json'
    json_utils.write_json(data, jsonName)
    graphspace_utils.postGraph(name, jsonName, 'menzelk@reed.edu', 'sirstoat')
    #graphspace_utils.shareGraph(name,'menzelk@reed.edu','sirstoat','Lab7','aritz@reed.edu')



def main():
    badgers, matrix = readIn()
    #graphit('testStatus', matrix, badgers)
    edges = readInEdges('GN-raw-list')
    groups = GNGroups(edges, matrix, 8)




if __name__ == '__main__':
    main()
