import graphspace_utils, json_utils, gen_utils


def readIn():
    File = open('BadgerMartix.txt')
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
        badgerDemo[row[0]] = {head[1]:row[1], head[2]:row[2]}

    matrix = matrix.split('\t')
    badgers = matrix.pop(0)
    badger = badgers.split('\t')
    badgers.pop(0)
    network = {}
    for i in range(len(matrix)):
        row = matrix[i].split('\t')
        badger = row.pop(0)
        for j in range(len(badgers)):
            network[badger][badgers[j]] = row[j]

    return badgerDemo, network
