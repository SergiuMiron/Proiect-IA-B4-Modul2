import json
import sys
import random
import Articulation
import Difficulty
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

def multiple_choice_first_type_of_question(nr_questions):
    try:
        #subjects = get_data_from_json("fisier1_subiecte.txt")
        nr_questions = min(int(nr_questions), len(subjects))
        #random.shuffle(subjects)

        answer_id_file =  open(r'C:\Users\Sergiu\Desktop\answers_vm.txt','w', encoding = "utf-8-sig")
        question_id_file = open(r'C:\Users\Sergiu\Desktop\questions_vm.txt','w', encoding = "utf-8-sig")
        answer_id = 0
        question_id = 0

        #Primul tip de intrebare
        for inst in subjects:
            if inst["noduri_legate"] != []:
                if inst["arc_nod"].count("contine") > 0 and inst["arc_nod"].count("contine") == len(inst["arc_nod"]):
                    words = inst["nume"].split()
                    randoms = [0, 1, 2]
                    dificultate = 0
                    if len(words) > 1:
                        words[0] = Articulation.ArticulateWord(words[0])
                        question_id = question_id + 1
                        words = " ".join(words)
                        question = [question_id,inst["domeniu"],0,"Ce componenta face parte parte din " + words + "?",0]

                    else:
                        question_id = question_id + 1
                        question = [question_id, inst["domeniu"], 0, "Ce componenta face parte parte din " + inst["nume"].lower() + "?", 0]

                    bool = True
                    nr_raspunsuri_corecte = 1
                    nr_raspunsuri_totale = 1
                    for id_nod in inst["noduri_legate"]:
                             x = [i for i in subjects if i["id"] == id_nod]
                             if nr_raspunsuri_corecte <= 3:
                                if x != []:
                                    x = x[0]
                                   # if ( x["arc_nod"] == ["contine"]):
                                    dificultate = Difficulty.diffBasedOnNodeDepth(subjects[0]["id"],id_nod,subjects)
                                    bool = True
                                    nr_raspunsuri_corecte = nr_raspunsuri_corecte + 1
                                    nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                                    answer_id = answer_id + 1
                                    answer = [answer_id, question_id,x["nume"].lower(),bool ]
                                    question[2] = dificultate
                                    answer_id_file.write(str(answer))
                                    answer_id_file.write("\n")
                    question_id_file.write(str(question))
                    question_id_file.write("\n")
                    nr_questions = nr_questions - 1
                    for id_nod in inst["noduri_legate"]:
                             while (nr_raspunsuri_totale <= 5):
                                 y = [i for i in subjects if i["id"] != id_nod]
                                 y05 = [i["id"] for i in subjects if i["id"] != id_nod]
                                 y2 = [0 for i in range(0,max(y05) + 1)]
                                 random.shuffle(y)
                                 while y2[y[0]["id"]] == 1:
                                     random.shuffle(y)
                                 y2[y[0]["id"]] = 1
                                 if y != []:
                                     y = y[0]
                                     bool = False
                                     nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                                     answer_id = answer_id + 1
                                     answer = [answer_id,question_id,y["nume"].lower(),bool]
                                     answer_id_file.write(str(answer))
                                     answer_id_file.write("\n")
            if nr_questions == 0:
                break

        #Al doilea tip de intrebare
        for inst in subjects:
            if inst["noduri_legate"] != []:
                if inst["arc_nod"].count("de_tip") > 0 and inst["arc_nod"].count("de_tip") == len(inst["arc_nod"]):
                    randoms = [0, 1, 2]
                    random.shuffle(randoms)
                    question_id = question_id + 1
                    question = [question_id, inst["domeniu"], 0,
                                "Care dintre urmatoarele variante sunt tipuri de  " + inst["nume"].lower() + "?", 0]

                    bool = True
                    nr_raspunsuri_corecte = 1
                    nr_raspunsuri_totale = 1
                    # print(inst["noduri_legate"])
                    for id_nod in inst["noduri_legate"]:
                        # if(len(inst["noduri_legate"]) == 1)
                        # nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                        x = [i for i in subjects if i["id"] == id_nod]
                        y = [i for i in subjects if i["id"] != id_nod]
                        random.shuffle(y)
                        if nr_raspunsuri_corecte <= 3:
                            if x != []:
                                x = x[0]
                                dificultate = Difficulty.diffBasedOnNodeDepth(subjects[0]["id"],id_nod, subjects)
                                # if ( x["arc_nod"] == ["contine"]):
                                bool = True
                                nr_raspunsuri_corecte = nr_raspunsuri_corecte + 1
                                nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                                # print(x["nume"])
                                # print(inst["nume"])
                                # print(inst["id"])
                                question[2] = dificultate
                                answer_id = answer_id + 1
                                answer = [answer_id, question_id, x["nume"], bool]
                                answer_id_file.write(str(answer))
                                answer_id_file.write("\n")
                        if (nr_raspunsuri_totale <= 5):
                            if y != []:
                                y = y[0]
                                bool = False
                                nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                                answer_id = answer_id + 1
                                answer = [answer_id, question_id, y["nume"], bool]
                                answer_id_file.write(str(answer))
                                answer_id_file.write("\n")
                    question_id_file.write(str(question))
                    question_id_file.write("\n")
                    nr_questions = nr_questions - 1

            if nr_questions == 0:
                break

        #Al 3-lea tip de intrebare
        for inst in subjects:
            if inst["definitie"] != "":
                # print(inst["definitie"])
                randoms = [0, 1, 2]
                random.shuffle(randoms)
                question_id = question_id + 1
                question = [question_id, inst["domeniu"], 0,
                            "Care dintre urmatoarele variante poate fi considerata o definitie a termenului: " + inst[
                                "nume"], 0]
                bool = True
                nr_raspunsuri_corecte = 0
                nr_raspunsuri_totale = 0
                if nr_raspunsuri_corecte < 1:
                    bool = True
                    dificultate = Difficulty.diffBasedOnNodeDepth(subjects[0]["id"],inst["id"], subjects)
                    question[2] = dificultate
                    nr_raspunsuri_corecte = nr_raspunsuri_corecte + 1
                    nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id, inst["definitie"], bool]
                    answer_id_file.write(str(answer))
                    answer_id_file.write("\n")
                while (nr_raspunsuri_totale <= 3):
                    bool = False
                    x = [i for i in subjects if i["definitie"] != inst["definitie"] and i["definitie"] != ""]
                    random.shuffle(x)
                    x = x[0]
                    nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id, x["definitie"], bool]
                    answer_id_file.write(str(answer))
                    answer_id_file.write("\n")

                question_id_file.write(str(question))
                question_id_file.write("\n")
                nr_questions = nr_questions - 1

            if nr_questions == 0:
                break


        question_id_file.close()
        answer_id_file.close()


    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Cannot open file")
    except ValueError:
        print("Wrong data type for nr of questions")
    except Exception as e:
        print(e)

multiple_choice_first_type_of_question(30)