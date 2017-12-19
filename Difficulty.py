import json
import sys

if "Difficulty" not in sys.modules:
    with open(r'C:\Users\Mircius\Desktop\Inteligenta Artificiala\Proiect-IA-B4-Modul2\fisier1_subiecte.txt', 'r',
              encoding="utf-8-sig") as data_file:
        json_data_subiecte = data_file.read()

    subjects = json.loads(json_data_subiecte)

# Assume there is a global "subjects" json list

# Dificultate bazata pe distanta;
# Exemplu: daca nodul dat drept raspuns se afla in prima treime, plecand de la radacina ontologiei, va fi un raspuns usor
# Easy: 0-33%
# Medium: 33%-66%
# Hard: 66%-100%

def getEntryIndexById (node_id):
    for index in range(0, len(subjects)):
        if subjects[index]['id'] == node_id:
            return index
    return -1

#assume the first node(entry) is the JSON is ontology's root node
# TODO Maybe the DB id should be passed as argument?
def calculateMaxDepth(root):
    max = 0
    for node in subjects[root]['noduri_legate']:
        currentMax = calculateMaxDepth(getEntryIndexById(node))
        if currentMax > max:
            max = currentMax

    return max + 1

# TODO Call get Entry index before
def calculateNodeDepth(current_node, answer_node_id, current_depth):
    if current_node == getEntryIndexById(answer_node_id):
        return current_depth
    tmp =0
    for node in subjects[current_node]['noduri_legate']:
        tmp+=calculateNodeDepth(getEntryIndexById(node), answer_node_id, current_depth+1)
    return tmp

#there should be "road" from the root to any of the nodes
# 0 - Easy, 1 - Medium, 2 - Hard
# !! Node_id is the id from the ontology, not the index in the subjects file !!
def diffBasedOnNodeDist(node_id):
   maxDepth = calculateMaxDepth(0)
   nodeDepth = calculateNodeDepth(0, node_id, 0)
   print(maxDepth, nodeDepth)
   difficulty = nodeDepth * 100 / maxDepth;
   if difficulty < 33.3:
       return 0
   elif difficulty > 33.3 and difficulty < 66.6:
       return 1
   else: return 2