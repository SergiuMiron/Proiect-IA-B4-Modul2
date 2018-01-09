import json
import sys
from Difficulty import diffBasedOnNodeDepth
with open('fisier1_subiecte.txt', 'r', encoding="utf-8-sig") as data_file:
    json_data_subiecte = data_file.read()

with open('fisier2_proprietati.txt', 'r', encoding="utf-8-sig") as data_file:
    json_data_proprietati = data_file.read()

subjects = json.loads(json_data_subiecte)
properties = json.loads(json_data_proprietati)

def GeneratingMatching():
	question_id = 0
	answer_id = 0
	question_id_file = open('matching_q_synonyms.txt', 'w',
                        encoding="utf8")
	answer_id_file = open('matching_a_synonyms.txt', 'w',
                      encoding="utf8")
	# Match by synonyms
	for inst in subjects:
	    if inst["sinonime"] != []:
	        question_id = question_id + 1
	        difficultate = diffBasedOnNodeDepth(subjects[0]["id"],inst["id"],subjects)
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


	question_id_file = open('matching_q_properties.txt', 'w',
	                        encoding="utf8")
	answer_id_file = open('matching_a_properties.txt', 'w',
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
	                difficultate = diffBasedOnNodeDepth(subjects[0]["id"],x["id"],subjects)
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


	question_id_file = open('matching_q_definition.txt', 'w',
	                        encoding="utf8")
	answer_id_file = open('matching_a_definition.txt', 'w',
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
	            difficultate = diffBasedOnNodeDepth(subjects[0]["id"],inst["id"],subjects)
	            question = [question_id, inst["domeniu"],difficultate,inst["nume"],"SingleMathch"]
	            questions_definitions.append(question)
	            answer = [answer_id,question_id,inst["definitie"],1]
	            answers_definitions.append(answer)

	            answer_id_file.write(str(answer)+ "\n")
	            question_id_file.write(str(question) + "\n")

GeneratingMatching()