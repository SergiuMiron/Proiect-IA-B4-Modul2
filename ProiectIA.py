import json
import random



#TODO - CHECK FOR DUPLICATES IN QUESTIONS/ANSWERS - FIND A WAY TO MEASURE DIFFICULTY - MATCH BY SPLITTING THE DEFINITIONS OF A SUBJECT IN TWO


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

for inst in subjects:
    if inst["noduri_legate"] != []:
        question_id = question_id + 1
        question = [question_id,inst["domeniu"],"Easy","Ce componenta face parte din " + inst["nume"],"Variante multiple"]

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






question_id_file.close()
answer_id_file.close()
















