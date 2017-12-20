import json
import sys
import pathlib


if "Difficulty" not in sys.modules:
    with open(str(pathlib.Path(__file__).parent) + '\\fisier1_subiecte.json', 'r',
              encoding="utf-8-sig") as data_file:
        json_data_subiecte = data_file.read()

    subjects = json.loads(json_data_subiecte)

# Assume there is a global "subjects" json list

# Dificultate bazata pe distanta;
# Exemplu: daca nodul dat drept raspuns se afla in prima treime, plecand de la radacina ontologiei, va fi un raspuns usor
# Easy: 0-33%
# Medium: 33%-66%
# Hard: 66%-100%

# Cauta indexul din json corespunzator id-ului cautat din baza de date
def getEntryIndexById (node_id):
    for index in range(0, len(subjects)):
        if subjects[index]['id'] == node_id:
            return index
    return -1

# TODO Maybe the DB id should be passed as argument?
# Calculeaza inaltimea maxima incepand de la root, care este indexul din fisierul json!
def calculateMaxDepth(root):
    max = 0
    for node in subjects[root]['noduri_legate']:
        currentMax = calculateMaxDepth(getEntryIndexById(node))
        if currentMax > max:
            max = currentMax

    return max + 1
#Example:
#print(calculateMaxDepth(getEntryIndexById(100)))

# TODO Optimise callind getEntryIndex
# Calculeaza distanta de la root_node la answer_node_id
# !! Deoarece fisierul nostru cu subiecte are mai multe concepte care nu sunt legate intre ele (ca in ontologia finala)
# !! Va trebui sa dati ca root_node conceptul in care vreti sa fie calculata distanta
def calculateNodeDepth(root_node, answer_node_id, current_depth):
    if root_node == getEntryIndexById(answer_node_id):
        return current_depth
    tmp =0
    for node in subjects[root_node]['noduri_legate']:
        tmp+=calculateNodeDepth(getEntryIndexById(node), answer_node_id, current_depth+1)
    return tmp

# Exemplu apel: cautam subiectul cu id-ul 500 luand ca radacina a conceptului nodul cu id-ul 100 din fisier
#print (calculateNodeDepth(getEntryIndexById(100),500, 0))

#there should be "road" from the root to any of the nodes
# 0 - Easy, 1 - Medium, 2 - Hard
# !! Root_id and Node_id is the id from the ontology, not the index in the subjects file !!
def diffBasedOnNodeDist(root_id, node_id):
   maxDepth = calculateMaxDepth(getEntryIndexById(root_id))
   nodeDepth = calculateNodeDepth(getEntryIndexById(root_id), node_id, 0)
   difficulty = nodeDepth * 100 / maxDepth
   if difficulty < 33.3:
       return 0
   elif difficulty > 33.3 and difficulty < 66.6:
       return 1
   else: return 2