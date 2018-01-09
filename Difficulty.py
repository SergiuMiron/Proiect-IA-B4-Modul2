import json
import sys

# Assume there is a global "subjects" json list

# Dificultate bazata pe distanta;
# Exemplu: daca nodul dat drept raspuns se afla in prima treime, plecand de la radacina ontologiei, va fi un raspuns usor
# Easy: 0-33% ( Value 0)
# Medium: 33%-66% (Value 1)
# Hard: 66%-100% (Value 2)

# Cauta indexul din json corespunzator id-ului cautat din baza de date
def getEntryIndexById (node_id, subjects):
    for index in range(0, len(subjects)):
        if subjects[index]['id'] == node_id:
            return index
    return -1

# TODO Maybe the DB id should be passed as argument?
# Calculeaza inaltimea maxima incepand de la root, care este indexul din fisierul json!
def calculateMaxDepth(root, subjects):
    max = 0
    for node in subjects[root]['noduri_legate']:
        currentMax = calculateMaxDepth(getEntryIndexById(node, subjects), subjects)
        if currentMax > max:
            max = currentMax

    return max + 1
# Example:
# print(calculateMaxDepth(getEntryIndexById(100, subjects), subjects))

# TODO Optimise callind getEntryIndex
# Calculeaza distanta de la root_node la answer_node_id
# !! Deoarece fisierul nostru cu subiecte are mai multe concepte care nu sunt legate intre ele (ca in ontologia finala)
# !! Va trebui sa dati ca root_node conceptul in care vreti sa fie calculata distanta
def calculateNodeDepth(root_node, answer_node_id, current_depth, subjects):
    if root_node == getEntryIndexById(answer_node_id, subjects):
        return current_depth
    tmp =0
    for node in subjects[root_node]['noduri_legate']:
        tmp+=calculateNodeDepth(getEntryIndexById(node, subjects), answer_node_id, current_depth+1, subjects)
    return tmp

# Exemplu apel: cautam subiectul cu id-ul 500 luand ca radacina a conceptului nodul cu id-ul 100 din fisier
# print (calculateNodeDepth(getEntryIndexById(100, subjects),500, 0, subjects))

# there should be "road" from the root to any of the nodes
# !! Root_id and Node_id is the id from the ontology, not the index in the subjects file !!
def diffBasedOnNodeDepth(root_id, node_id, subjects):
   maxDepth = calculateMaxDepth(getEntryIndexById(root_id,subjects), subjects)
   nodeDepth = calculateNodeDepth(getEntryIndexById(root_id,subjects), node_id, 0, subjects)
   difficulty = nodeDepth * 100 / maxDepth;
   if difficulty < 33.3:
       return 0
   elif difficulty > 33.3 and difficulty < 66.6:
       return 1
   else: return 2

# Floyd–Warshall algorithm implementation for finding the distance between any 2 nodes in the ontology

# TODO Assume the ontology is like a tree??
# Returns a dictionary containing the distances between every node of the ontology
# Example dict[(node_1, node_2)] is the distance between node_1 and node_2
def calculateDistBetweenNodes(root_node_id, subjects):
    distances = dict()
    nodes = list()

    def getEdges(root_node_id):
        nodes.append(root_node_id)
        distances[(root_node_id, root_node_id)] = 0
        for node in subjects[getEntryIndexById(root_node_id, subjects)]['noduri_legate']:
            distances[(root_node_id, node)] = 1
            distances[(node, root_node_id)] = 1
            getEdges(node)

    getEdges(root_node_id)

    for i in range (0,len(nodes)):
        for j in range (0, len(nodes)):
            if (nodes[i], nodes[j]) not in distances:
                distances[(nodes[i], nodes[j])] = float('Inf')

    for k in range (0,len(nodes)):
        for i in range (0,len(nodes)):
            for j in range (0,len(nodes)):
                if distances[(nodes[i],nodes[j])] > distances[(nodes[i],nodes[k])] + distances[(nodes[k],nodes[j])]:
                    distances[(nodes[i],nodes[j])] = distances[(nodes[i],nodes[k])] + distances[(nodes[k],nodes[j])]

    return distances

# Returs the difficulty based on the distance between two nodes
def diffBasedOnNodeDist(root_id, first_node, second_node, subjects):
   distances = calculateDistBetweenNodes(root_id, subjects)
   difficulty = distances[(first_node, second_node)] * 100 / max(distances.values());
   print(distances)
   print(distances[(first_node, second_node)])
   print(max(distances.values()))
   if difficulty < 33.3:
       return 0
   elif difficulty > 33.3 and difficulty < 66.6:
       return 1
   else: return 2



