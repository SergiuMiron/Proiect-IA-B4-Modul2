import json
# TODO - CHECK FOR DUPLICATES IN QUESTIONS/ANSWERS - FIND A WAY TO MEASURE DIFFICULTY - MATCH BY SPLITTING THE DEFINITIONS OF A SUBJECT IN TWO


# Change path
with open(r'C:\Users\Vlad\Desktop\ProjectIA\fisier1_subiecte.txt', 'r', encoding="utf-8-sig") as data_file:
    json_data_subiecte = data_file.read()

with open(r'C:\Users\Vlad\Desktop\ProjectIA\fisier2_proprietati.txt', 'r', encoding="utf-8-sig") as data_file:
    json_data_proprietati = data_file.read()

subjects = json.loads(json_data_subiecte)
properties = json.loads(json_data_proprietati)

# O sa avem o lista de dictionare ( 1 dictionar = 1 json / o instanta )
print(type(subjects))
print(type(properties))

question_id = 0
answer_id = 0

import json
import sys

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
   print(maxDepth, nodeDepth)
   difficulty = nodeDepth * 100 / maxDepth;
   if difficulty < 33.3:
       return 0
   elif difficulty > 33.3 and difficulty < 66.6:
       return 1
   else: return 2


# Create files for testing question_id / answer_id

question_id_file = open(r'C:\Users\Vlad\Desktop\ProjectIA\questions_synonyms.txt', 'w',
                        encoding="utf8")
answer_id_file = open(r'C:\Users\Vlad\Desktop\ProjectIA\answers_synonyms.txt', 'w',
                      encoding="utf8")

# Match by synonyms
for inst in subjects:
    if inst["sinonime"] != []:
        question_id = question_id + 1
        difficultate = diffBasedOnNodeDist(subjects[0]["id"],inst["id"])
        question = [question_id, inst["domeniu"], difficultate, inst["nume"], "SingleMatch"]
        # print(inst["nume"])

        question_id_file.write(str(question))
        question_id_file.write("\n")
        x = inst["sinonime"]
        # print(x)

        for sinonim in x:
            answer_id = answer_id + 1;
            answer = [answer_id, question_id, sinonim, "True"]
            answer_id_file.write(str(answer))
            answer_id_file.write("\n")


        # print("\n\n\n")

question_id_file.close()
answer_id_file.close()


question_id_file = open(r'C:\Users\Vlad\Desktop\ProjectIA\questions_properties.txt', 'w',
                        encoding="utf8")
answer_id_file = open(r'C:\Users\Vlad\Desktop\ProjectIA\answers_properties.txt', 'w',
                      encoding="utf8")

# Match by properties
questions_properties = []
answers_properties = []
for inst in properties:
    if inst["id_sub"] != []:
        #print (inst["id_sub"])
        for id_subiect in inst["id_sub"]:
            #print(id_subiect)
            x = [i for i in subjects if i["id"] == id_subiect]
            if x != []:
                x = x[0]
                question_id = question_id + 1
                difficultate = diffBasedOnNodeDist(subjects[0]["id"],x["id"])
                question = [question_id, x["domeniu"], difficultate, x["nume"], "SingleMatch"]

                answer_id = answer_id + 1
                answer = [answer_id, question_id, inst["nume"], "True"]

                questions_properties.append(question)
                answers_properties.append(answer)

#remove duplicate questions
for i in questions_properties:
    dup = [j for j in questions_properties if i[3] == j[3] and i[1] == j[1] and i[0] != j[0]]
    for k in dup:
        answer = [x for x in answers_properties if k[0] == x[1]]
        answer[0][1] = i[0]
    for k in dup:
        questions_properties.remove(k)

#write to file
for i in questions_properties:
    question_id_file.write(str(i) + "\n")
for i in answers_properties:
    answer_id_file.write(str(i) + "\n")

question_id_file.close()
answer_id_file.close()


question_id_file = open(r'C:\Users\Vlad\Desktop\ProjectIA\questions_definition.txt', 'w',
                        encoding="utf8")
answer_id_file = open(r'C:\Users\Vlad\Desktop\ProjectIA\answers_definition.txt', 'w',
                      encoding="utf8")


answers_definitions = []
questions_definitions = []
# Match by splitting the definitions of a subject - TODO
for inst in subjects:
    if inst["definitie"] != "":
        question = [i for i in questions_properties if i[1] == inst["domeniu"] and i[3] == inst["nume"]]
        answer_id += 1
        if question != []:
            answer = [answer_id, question[0][0],inst["definitie"],1]
            answers_definitions.append(answer)
            answer_id_file.write(str(answer)+ "\n")
        else:
            question_id += 1
            difficultate = diffBasedOnNodeDist(subjects[0]["id"],inst["id"])
            question = [question_id, inst["domeniu"],difficultate,inst["nume"],"SingleMathch"]
            questions_definitions.append(question)
            answer = [answer_id,question_id,inst["definitie"],1]
            answers_definitions.append(answer)

            answer_id_file.write(str(answer)+ "\n")
            question_id_file.write(str(question) + "\n")