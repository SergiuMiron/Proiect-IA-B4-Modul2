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


# Intrebari pe baza definitiei, cautam dupa cuvintele cheie: "este", "defineste", "reprezinta".
# Intrebari usoare, cu un singur raspuns corect, mai exact definitia
# Merge destul de greut, raman de vazut de ce
# First type of questions
random.shuffle(subjects)
for inst in subjects:
    #if inst["definitie"].startswith("Este") or inst["definitie"].startswith("este"):
    if "este" in inst["definitie"] or "Este" in inst["definitie"]:
        answer_data = inst["nume"]
        question_data = str.lower(inst["definitie"])
        if inst["definitie"].startswith("Este"):
            question_data_final = question_data
        else:
            index_space = question_data.index("este")
            question_data_final = question_data[index_space:]
        # Verific doar cuvintele ce le pot articula (fara diacritice si care exista in dex)
        # Definitiile formate din 2 cuvinte -> il articulez doar pe primul ("margine anterioara -> marginea anterioara")
        if answer_data.count(" ") == 0:
            if ArticulateWord(str.lower(answer_data)) is not None:
                if str(ArticulateWord(str.lower(answer_data))) != "Eroare":
                    answer_data_final = ArticulateWord(str.lower(answer_data)).title()
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id + 1, answer_data_final, True]
                    answer_id_file.write(str(answer) + '\n')
        else:
            index_space = answer_data.index(" ")
            first_word = answer_data[0:index_space]
            if ArticulateWord(str.lower(first_word)) is not None:
                if str(ArticulateWord(str.lower(first_word))) != "Eroare":
                    answer_data_final = ArticulateWord(str.lower(first_word)).title() + answer_data[index_space:]
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id + 1, answer_data_final, True]
                    answer_id_file.write(str(answer) + '\n')

        # daca am putut construi un raspuns valid adaugam si intrebarea
        if question_id < answer_id:
            question_id = question_id + 1
            question = [question_id, inst["domeniu"], "Easy", "... " + question_data_final, "FITB"]
            question_id_file.write(str(question) + '\n')


question_id_file.close()
answer_id_file.close()

