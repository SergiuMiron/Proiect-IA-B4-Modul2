import json
import random
import pathlib
import Articulation
import Difficulty


def get_data_from_json(filename):
    try:
        file = open(r'C:\Users\Sergiu\Desktop\fisier1_subiecte.txt',  'r' , encoding = "utf-8-sig")
        to_return = json.loads(file.read())
        return to_return
    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Cannot open file")
    except Exception as e:
        print(e)


def multiple_choice_first_type_of_question(nr_questions):
    try:
        subjects = get_data_from_json("fisier1_subiecte.txt")
        nr_questions = min(int(nr_questions), len(subjects))
        #random.shuffle(subjects)

        answer_id_file =  open(r'C:\Users\Sergiu\Desktop\answers_vm.txt','w', encoding = "utf-8-sig")
        question_id_file = open(r'C:\Users\Sergiu\Desktop\questions_vm.txt','w', encoding = "utf-8-sig")
        answer_id = 0
        question_id = 0

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
                                    dificultate = Difficulty.diffBasedOnNodeDist(id_nod,subjects)
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
                                dificultate = Difficulty.diffBasedOnNodeDist(id_nod, subjects)
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
                    dificultate = Difficulty.diffBasedOnNodeDist(inst["id"], subjects)
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

multiple_choice_first_type_of_question(25)






















