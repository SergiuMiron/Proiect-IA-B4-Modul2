
# Assume there is a global "subjects" json list

# Dificultate bazata pe distanta;
# Exemplu: daca nodul dat drept raspuns se afla in prima treime, plecand de la radacina ontologiei, va fi un raspuns usor
# Easy: 0-33%
# Medium: 33%-66%
# Hard: 66%-100%

def getEntryIndexById (node_id,subjects):
    for index in range(0, len(subjects)):
        if subjects[index]['id'] == node_id:
            return index
    return -1

#assume the first node(entry) is the JSON is ontology's root node
# TODO Maybe the DB id should be passed as argument?
def calculateMaxDepth(root,subjects):
    max = 0
    for node in subjects[root]['noduri_legate']:
        currentMax = calculateMaxDepth(getEntryIndexById(node,subjects),subjects)
        if currentMax > max:
            max = currentMax
    return max + 1

# TODO Call get Entry index before
def calculateNodeDepth(current_node, answer_node_id, current_depth,subjects):
    if current_node == getEntryIndexById(answer_node_id,subjects):
        return current_depth
    tmp =0
    for node in subjects[current_node]['noduri_legate']:
        tmp+=calculateNodeDepth(getEntryIndexById(node,subjects), answer_node_id, current_depth+1,subjects)
    return tmp

#there should be "road" from the root to any of the nodes
# 0 - Easy, 1 - Medium, 2 - Hard
# !! Node_id is the id from the ontology, not the index in the subjects file !!
def diffBasedOnNodeDist(node_id,subjects):

   maxDepth = calculateMaxDepth(0,subjects)
   nodeDepth = calculateNodeDepth(0, node_id, 0,subjects)
   #print("data",maxDepth, nodeDepth)
   difficulty = nodeDepth * 100 / maxDepth;
   if difficulty < 1.3:
       return 0
   elif difficulty > 1.3 and difficulty < 66.6:
       return 1
   else:
       return 2