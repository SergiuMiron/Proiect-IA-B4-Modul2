import json
import random
from Articulation import ArticulateWord


#Change path
with open(r'C:\Users\razva\Desktop\Fill_in_the_blanks\fisier1_subiecte.txt',  'r' , encoding = "utf-8-sig") as data_file:
    json_data_subiecte = data_file.read()

with open(r'C:\Users\razva\Desktop\Fill_in_the_blanks\fisier2_proprietati.txt', 'r', encoding="utf-8-sig") as data_file:
    json_data_proprietati = data_file.read()

subjects = json.loads(json_data_subiecte)
properties = json.loads(json_data_proprietati)

#Create files for testing question_id / answer_id

question_id_file = open(r'C:\Users\razva\Desktop\Fill_in_the_blanks\questions_vm.txt', 'w', encoding="utf-8-sig")
answer_id_file =  open(r'C:\Users\razva\Desktop\Fill_in_the_blanks\answers_vm.txt', 'w', encoding="utf-8-sig")

question_id = 0
answer_id = 0

#1st type of questions (complete the definition):
random.shuffle(subjects)
for inst in subjects:
    if inst["definitie"].startswith("Este") or inst["definitie"].startswith("este"):
        answer_data = inst["nume"]
        question_data = str.lower(inst["definitie"])
        # verific doar cuvintele ce le pot articula (fara diacritice si care exista in dex)
        # momentan pornesc de la premiza ca definitiile cu 2-3 cuvinte in nume sunt deja articulate ("ex: Cutia craniana")
        if answer_data.count(" ") == 0:
            if ArticulateWord(str.lower(answer_data)) is not None:
                if str(ArticulateWord(str.lower(answer_data))) != "Eroare":
                    answer_data_final = ArticulateWord(str.lower(answer_data)).title()
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id + 1, answer_data_final, True]
                    answer_id_file.write(str(answer) + '\n')
        else:
            answer_data_final = answer_data
            answer_id = answer_id + 1
            answer = [answer_id, question_id + 1, answer_data_final, True]
            answer_id_file.write(str(answer) + '\n')

        # daca am putut construi un raspuns valid adaugam si intrebarea
        if question_id < answer_id:
            question_id = question_id + 1
            question = [question_id, inst["domeniu"], "Easy", "... " + question_data, "FITB"]
            question_id_file.write(str(question) + '\n')


question_id_file.close()
answer_id_file.close()


