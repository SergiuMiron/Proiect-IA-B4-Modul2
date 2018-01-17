import json
import sys

if "Difficulty" not in sys.modules:
    with open(r'C:\Users\Mircius\Desktop\Inteligenta Artificiala\Proiect-IA-B4-Modul2\fisier1_subiecte.txt', 'r',
              encoding="utf-8-sig") as data_file:
        json_data_subiecte = data_file.read()

    subjects = json.loads(json_data_subiecte)

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

# there should be a "road" from the root to any of the nodes
# !! Root_id and Node_id is the id from the ontology, not the index in the subjects file !!
def diffBasedOnNodeDepth(root_id, node_id, subjects):
   maxDepth = calculateMaxDepth(getEntryIndexById(root_id,subjects), subjects)
   nodeDepth = calculateNodeDepth(getEntryIndexById(root_id,subjects), node_id, 0, subjects)
   difficulty = nodeDepth * 100 / maxDepth

   return difficulty

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

    print(distances)
    if max(distances.values()) == 0:
       return 0

    # daca al doilea nod nu exista in subarborele root_id, atunci va fi o intrebare usoara
    if (first_node, second_node) not in distances.keys():
       return 0

    difficulty = distances[(first_node, second_node)] * 100 / max(distances.values());

    return difficulty

# Levenshtein distance implementation

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# !! First and second node id the id from the ontology, not the index in the subjects file !!
def diffBasedOnLevDist(first_node_id, second_node_id, subjects):
    first_name = subjects[getEntryIndexById(first_node_id, subjects)]["nume"]
    second_name = subjects[getEntryIndexById(second_node_id, subjects)]["nume"]

    difference = levenshtein(first_name, second_name)
    max_diff = max(len(first_name), len(second_name))

    difficulty = difference * 100 / max_diff
    difficulty = 100 - difficulty

    return difficulty


# TODO Tweak difficulties "weight"
# TODO Check false answer

# ! Acesta este singura functie care trebuie folosita pentru dificultate !
# Al doilea argument trebuie sa fie TRUE daca, in cazul intrebarilor cu True/False, raspunsul e False

# !!! Se transmit ID-urile si NU index-ul din json !!!
# Numarul de raspunsuri este variabil

def computeDifficulty( subjects, bIsFalseAnswer, questionNode, *answerNodes):

    if getEntryIndexById(questionNode, subjects) == -1:
        print("ID-ul intrebarii nu exista")
        return

    for node in answerNodes:
        if getEntryIndexById(node, subjects) == -1:
            print("ID-ul" + str(node) + "nu exista")
            return

    rootDistDiff = diffBasedOnNodeDepth(12, questionNode, subjects)
    print (rootDistDiff)

    baseDistDiff = 0
    baseDistDiffCounter = 0
    for indx in range(0, len(answerNodes)):
        if bIsFalseAnswer == True: # o intrebare cu raspuns fals este mai grea daca conceptul este cat mai aproape de baza
            baseDistDiff += (100 - diffBasedOnNodeDist(questionNode, questionNode, answerNodes[indx], subjects))
        else: baseDistDiff += diffBasedOnNodeDist(questionNode, questionNode, answerNodes[indx], subjects)
        baseDistDiffCounter+= 1
        print("baseDistDiff:" + str(baseDistDiff) )

    if baseDistDiffCounter!= 0:
        baseDistDiff = baseDistDiff / baseDistDiffCounter
        print("baseDistDiff_final :" + str(baseDistDiff))

    levDiff = 0
    levDiffCounter = 0
    for indx1 in range(0, len(answerNodes)- 1):
        for indx2 in range (indx1 + 1, len(answerNodes)):
            levDiffTemp = diffBasedOnLevDist(answerNodes[indx1], answerNodes[indx2], subjects)
            # daca cuvintele sunt identice (diff == 100), intrebarea nu are rost, adica este usoara
            if levDiffTemp != 100:
                levDiff += levDiffTemp
            levDiffCounter+= 1
            print ("levDiff: " + str(levDiff))

    if levDiffCounter != 0:
        levDiff = levDiff / levDiffCounter
        print("levDiff_final: " + str(levDiff))

    finalDiff = 0.5 * rootDistDiff + 0.25 * baseDistDiff + 0.25 * levDiff
    print (finalDiff)

    if finalDiff < 33.3:
        return 0
    elif finalDiff > 33.3 and finalDiff < 66.6:
        return 1
    else: return 2

print(computeDifficulty(subjects, False, 12, 31))