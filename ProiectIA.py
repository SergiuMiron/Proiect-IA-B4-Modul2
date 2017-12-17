import json
import random
import Articulation


#Change path
with open(r'C:\Users\Sergiu\Desktop\fisier1_subiecte.txt',  'r' , encoding = "utf8") as data_file:
    json_data_subiecte = data_file.read()

with open(r'C:\Users\Sergiu\Desktop\fisier2_proprietati.txt', 'r' , encoding = "utf8") as data_file:
    json_data_proprietati = data_file.read()

subjects = json.loads(json_data_subiecte)
properties = json.loads(json_data_proprietati)

#O sa avem o lista de dictionare ( 1 dictionar = 1 json / o instanta )
#print(type(subjects))
#print(type(properties))

question_id = 0
answer_id = 0

#Create files for testing question_id / answer_id

question_id_file = open(r'C:\Users\Sergiu\Desktop\questions_vm.txt','w', encoding = "utf8")
answer_id_file =  open(r'C:\Users\Sergiu\Desktop\answers_vm.txt','w', encoding = "utf8")

#First type of question
for inst in subjects:
    if inst["noduri_legate"] != []:
        if inst["arc_nod"].count("contine") > 0 and inst["arc_nod"].count("contine") == len(inst["arc_nod"]):
            question_id = question_id + 1
            question = [question_id,inst["domeniu"],"Easy","Ce componenta face parte parte din " + inst["nume"],"Variante multiple"]
            #print(Articulation.ArticulateWord(inst["nume"]))
            #word=inst["nume"].split()
            #print(word[0])


            question_id_file.write(str(question))
            question_id_file.write("\n")
            bool = True
            nr_raspunsuri_corecte = 1
            nr_raspunsuri_totale = 1
            #print(inst["noduri_legate"])
            for id_nod in inst["noduri_legate"]:
               # if(len(inst["noduri_legate"]) == 1)
                     #nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                     x = [i for i in subjects if i["id"] == id_nod]
                     y = [i for i in subjects if i["id"] != id_nod]
                     random.shuffle(y)
                     if nr_raspunsuri_corecte <= 3:
                        if x != []:
                            x = x[0]
                           # if ( x["arc_nod"] == ["contine"]):
                            bool = True
                            nr_raspunsuri_corecte = nr_raspunsuri_corecte + 1
                            nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                            #print(x["nume"])
                            #print(inst["nume"])
                            #print(inst["id"])
                            answer_id = answer_id + 1
                            answer = [answer_id, question_id,x["nume"],bool ]
                            answer_id_file.write(str(answer))
                            answer_id_file.write("\n")
                     if (nr_raspunsuri_totale <= 5):
                         if y != []:
                             y = y[0]
                             bool = False
                             nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                             answer_id = answer_id + 1
                             answer = [answer_id,question_id,y["nume"],bool]
                             answer_id_file.write(str(answer))
                             answer_id_file.write("\n")

#Second type of question
for inst in subjects:
    if inst["noduri_legate"] != []:
        if inst["arc_nod"].count("de_tip") > 0 and inst["arc_nod"].count("de_tip") == len(inst["arc_nod"]):
            question_id = question_id + 1
            question = [question_id,inst["domeniu"],"Easy","Care dintre urmatoarele variante sunt tipuri de  " + inst["nume"] + "?","Variante multiple"]

            question_id_file.write(str(question))
            question_id_file.write("\n")
            bool = True
            nr_raspunsuri_corecte = 1
            nr_raspunsuri_totale = 1
            #print(inst["noduri_legate"])
            for id_nod in inst["noduri_legate"]:
               # if(len(inst["noduri_legate"]) == 1)
                     #nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                     x = [i for i in subjects if i["id"] == id_nod]
                     y = [i for i in subjects if i["id"] != id_nod]
                     random.shuffle(y)
                     if nr_raspunsuri_corecte <= 3:
                        if x != []:
                            x = x[0]
                           # if ( x["arc_nod"] == ["contine"]):
                            bool = True
                            nr_raspunsuri_corecte = nr_raspunsuri_corecte + 1
                            nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                            #print(x["nume"])
                            #print(inst["nume"])
                            #print(inst["id"])
                            answer_id = answer_id + 1
                            answer = [answer_id, question_id,x["nume"],bool ]
                            answer_id_file.write(str(answer))
                            answer_id_file.write("\n")
                     if (nr_raspunsuri_totale <= 5):
                         if y != []:
                             y = y[0]
                             bool = False
                             nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                             answer_id = answer_id + 1
                             answer = [answer_id,question_id,y["nume"],bool]
                             answer_id_file.write(str(answer))
                             answer_id_file.write("\n")

#Third type of question
for inst in subjects:
    if inst["definitie"] != "":
            question_id = question_id + 1
            question = [question_id,inst["domeniu"],"Easy","Care dintre urmatoarele variante poate fi considerata o definitie a termenului: " + inst["nume"],"Variante multiple"]
            question_id_file.write(str(question))
            question_id_file.write("\n")
            bool = True
            nr_raspunsuri_corecte = 0
            nr_raspunsuri_totale = 0
            if nr_raspunsuri_corecte < 1:
               bool = True
               nr_raspunsuri_corecte = nr_raspunsuri_corecte + 1
               nr_raspunsuri_totale = nr_raspunsuri_totale + 1
               answer_id = answer_id + 1
               answer = [answer_id, question_id,inst["definitie"],bool ]
               answer_id_file.write(str(answer))
               answer_id_file.write("\n")
            while (nr_raspunsuri_totale <= 3):
                bool = False
                x = [i for i in subjects if i["definitie"] != inst["definitie"] and i["definitie"] != ""]
                random.shuffle(x)
                x = x[0]
                nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                answer_id = answer_id + 1
                answer = [answer_id,question_id,x["definitie"],bool]
                answer_id_file.write(str(answer))
                answer_id_file.write("\n")




question_id_file.close()
answer_id_file.close()
















