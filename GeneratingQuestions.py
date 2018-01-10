import json
import sys
import random
import Articulation
import Difficulty
from Difficulty import diffBasedOnNodeDepth
import pathlib
import WordGender
import Plural

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
	            question = [question_id, inst["domeniu"],difficultate,inst["nume"],"SingleMatch"]
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


# FILL IN QUESTIONS

def remove_duplicates(concepte):
    lista = list()
    nume = set()
    try:
        for dictionar in concepte:
            for key, value in dictionar.items():
                if key == "nume":
                    nume.add(value)
        for n in nume:
            for c in concepte:
                if n == c["nume"]:
                    lista.append(c)
                    break
        return lista
    except IndexError as e:
        print("Eroare: " + str(e))


def has_synonyms(concept):
    if len(concept["sinonime"]) > 0:
        return True
    else:
        return False


def generate_fill_in_by_definitions_questions(nr_questions):
    try:
        nr_questions = min(int(nr_questions), len(subjects))
        random.shuffle(subjects)

        answers_file = open(str(pathlib.Path(__file__).parent) + "\\fillin_a_definitions.txt", "w", encoding="utf-8-sig")
        questions_file = open(str(pathlib.Path(__file__).parent) + "\\fillin_q_definitions.txt", "w", encoding="utf-8-sig")

        answer_id = 0
        question_id = 0

        for inst in subjects:
            if "este" in inst["definitie"] or "Este" in inst["definitie"]:
                answer_data = inst["nume"]
                question_data = str.lower(inst["definitie"])
                if inst["definitie"].startswith("Este"):
                    question_data_final = question_data
                else:
                    index_space = question_data.index("este")
                    question_data_final = question_data[index_space:]

                if answer_data.count(" ") == 0:
                    answer_data_final = Articulation.ArticulateWord(answer_data).capitalize()
                    # print(answer_data_final)
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id + 1, answer_data_final, True]
                    answers_file.write(str(answer) + '\n')
                else:
                    index_space = answer_data.index(" ")
                    first_word = answer_data[0:index_space]
                    answer_data_final = Articulation.ArticulateWord(str.lower(first_word)).capitalize() + answer_data[index_space:]
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id + 1, answer_data_final, True]
                    answers_file.write(str(answer) + '\n')

                # Daca am putut construi un raspuns valid adaugam si intrebarea
                if question_id < answer_id:
                    question_id = question_id + 1
                    # al 3-lea argument este dificultatea: 0 - easy, 1 - medium, 2 - hard
                    question = [question_id, inst["domeniu"], Difficulty.diffBasedOnNodeDepth(subjects[0]["id"], inst["id"], subjects), "... " + question_data_final, "FillIn"]
                    questions_file.write(str(question) + '\n')
                    nr_questions = nr_questions - 1

                if nr_questions == 0:
                    break

        answers_file.close()
        questions_file.close()

    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Cannot open file")
    except ValueError:
        print("Wrong data type for nr of questions")
    except Exception as e:
        print(e)


def generate_question(concept_p):
    # print(concept_p["nume"])

    # Extragem cuvintele
    words_q = concept_p["nume"].split(' ')
    first_word = words_q[0].lower()
    gender = WordGender.WordGender(first_word)
    first_word_articulated = str(Articulation.ArticulateWord(first_word)).capitalize()
    word_plural = Plural.get_plural(first_word)

    if gender == "Unknown":
        gender = "masculin"

    question_statement = str(first_word_articulated) + ' '

    # In cazul in care avem mai multe cuvinte in numele conceptului,
    #  articulam doar primul cuvant si ii facem prima litera majuscula.
    if len(words_q) > 1:
        for index in range(1, len(words_q)):
            question_statement = question_statement + words_q[index] + ' '

    if gender == 'feminin':
        # Forma de feminin singular/plural
        if word_plural != first_word:
            question_statement = question_statement + "mai este cunoscută și sub numele de"
        else:
            question_statement = question_statement + "mai sunt cunoscute și sub numele de"
    elif gender == "masculin":
        # Forma de masculin singular/plural
        if word_plural != first_word:
            question_statement = question_statement + "mai este cunoscut și sub numele de"
        else:
            question_statement = question_statement + "mai sunt cunoscuți și sub numele de"
    else:
        # Forma de neutru singular/plural
        if word_plural != first_word:
            question_statement = question_statement + "mai este cunoscut și sub numele de"
        else:
            question_statement = question_statement + "mai sunt cunoscute și sub numele de"

    return question_statement


def generate_fill_in_by_synonyms_questions(nr_questions):
    # Elimin duplicatele. La mine, de exemplu,
    # apare de mai multe ori conceptul de Perete anterior (si posterior si superior etc)..
    result = remove_duplicates(subjects)

    answers_file = open(str(pathlib.Path(__file__).parent) + "\\fillin_a_synonyms.txt", "w", encoding="utf8")
    questions_file = open(str(pathlib.Path(__file__).parent) + "\\fillin_q_synonyms.txt", "w", encoding="utf8")
    fields_file = open(str(pathlib.Path(__file__).parent) + "\\fields.txt", "w", encoding="utf8")

    question_id = 0
    answer_id = 0
    field_id = 0
    all_fields = []

    for cpt in result:
        if has_synonyms(cpt):
            question_id += 1

            # Domeniu nou? Atunci il adaugam in lista tuturor domeniilor.
            if cpt["domeniu"] not in all_fields:
                field_id += 1
                all_fields.append(cpt["domeniu"])
                fields_file.write(str(field_id) + ",  " + cpt["domeniu"] + '\n')

            q_statement = generate_question(cpt)
            answer_difficulty = Difficulty.diffBasedOnNodeDepth(subjects[0]["id"], cpt["id"], subjects)

            # 1 -> Fill in question type
            questions_file.write('[' +
                str(question_id) + ",  " + str(field_id) + ",  " + str(answer_difficulty) +
                ",  " + q_statement + ",  " + str(1) + ']\n')

            for sinonim in cpt["sinonime"]:
                answer_id += 1

                answers_file.write(
                    '[' + str(answer_id) + ",  " + str(question_id) + ",  " + sinonim + ",  " + str(True) + ']\n')

            nr_questions -= 1

            if nr_questions == 0:
                break

    answers_file.close()
    questions_file.close()
    fields_file.close()


def generate_fill_in_questions(syns_questions, defs_questions):
    generate_fill_in_by_synonyms_questions(syns_questions)
    generate_fill_in_by_definitions_questions(defs_questions)

generate_fill_in_questions(10, 30)



def GenerateTrueFalse():
	question_id = 0
	answer_id = 0

	question_id_file = open("questions_tf.txt","w", encoding = "utf-8-sig")
	answer_id_file =  open("answers_tf.txt","w", encoding = "utf-8-sig")

	#Questions of type one
	#The field "definitie" is used for every instance, thus every answer will have to be "Adevarat" of type True
	#Marked as Easy

	bool = True
	random.shuffle(subjects)
	for inst in subjects:

		concept_name = str(inst["nume"].lower())
		if inst["definitie"] != "":
		
			#If there are more words in the concept, articulate the first word
			if " " in inst["nume"]:
				space_index = concept_name.index(" ")
				first_word = concept_name[0:space_index]
				if Articulation.ArticulateWord(first_word) is not None and Articulation.ArticulateWord(first_word) != "Eroare":
					rest = concept_name[space_index:] #the  other words in the concept
					question_id += 1
					question = [question_id, inst["domeniu"], 0, "Urmatoarea definitie despre " + Articulation.ArticulateWord(first_word) + rest + " este adevarata sau falsa?   " + inst["definitie"],  "TrueFalse"]	
					question_id_file.write(str(question))
					question_id_file.write("\n")
			else:
				question_id += 1
				question = [question_id, inst["domeniu"], 0, "Urmatoarea definitie despre " + concept_name + " este adevarata sau falsa?   " + inst["definitie"],  "TrueFalse"]	
				question_id_file.write(str(question))
				question_id_file.write("\n")
			
			#If the question has been created, then add the answer too
			if answer_id < question_id:
				answer_id += 1
				answer = [answer_id, question_id, "True", bool]
				answer_id_file.write(str(answer))
				answer_id_file.write("\n")


	#Second type of question

	#True questions
	for inst in subjects:

		concept_name = str(inst["nume"].lower())
		if len(inst["sinonime"]) > 0:
			for i in range(0,len(inst["sinonime"])):
				question_id += 1
				question = [question_id, inst["domeniu"], 0, "Conceptul " + concept_name + " este identic conceptului de " + str(inst["sinonime"][i].lower()), "TrueFalse"]	
				question_id_file.write(str(question))
				question_id_file.write("\n")
			
				#If the question has been created, then add the answer too
				answer_id += 1
				answer = [answer_id, question_id, "True", True]
				answer_id_file.write(str(answer))
				answer_id_file.write("\n")

				answer_id += 1
				answer = [answer_id, question_id, "False", False]
				answer_id_file.write(str(answer))
				answer_id_file.write("\n")
		
	#False question
	for inst in subjects:

		for inst2 in subjects:

			if (len(inst2["sinonime"]) > 0 and inst["nume"].lower()!=inst2["nume"].lower() and inst["domeniu"].lower() == inst2["domeniu"].lower()):
				i = random.randint(0,len(inst2["sinonime"])-1)
				question_id += 1
				question = [question_id, inst["domeniu"], 0, "Conceptul " + concept_name + " este identic conceptului de " + str(inst2["sinonime"][i].lower()), "TrueFalse"]	
				question_id_file.write(str(question))
				question_id_file.write("\n")
		
				#If the question has been created, then add the answer too
				answer_id += 1
				answer = [answer_id, question_id, "False", True]
				answer_id_file.write(str(answer))
				answer_id_file.write("\n")

				answer_id += 1
				answer = [answer_id, question_id, "True", False]
				answer_id_file.write(str(answer))
				answer_id_file.write("\n")


	question_id_file.close()
	answer_id_file.close()


GenerateTrueFalse()