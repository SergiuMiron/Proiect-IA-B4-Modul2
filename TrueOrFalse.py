import json
import random
from Articulation import ArticulateWord

#Path needs to be changed
with open(r"C:\Users\Alina Coca\Desktop\ia-project\Proiect-IA-B4-Modul2\fisier1_subiecte.txt",  "r" , encoding = "utf-8-sig") as data_file:
    json_data_subiecte = data_file.read()

with open(r"C:\Users\Alina Coca\Desktop\ia-project\Proiect-IA-B4-Modul2\fisier2_proprietati.txt", "r" , encoding = "utf-8-sig") as data_file:
    json_data_proprietati = data_file.read()
	
subjects = json.loads(json_data_subiecte)
properties = json.loads(json_data_proprietati)

question_id = 0
answer_id = 0

#Create files for testing question_id/answer_id

question_id_file = open(r"C:\Users\Alina Coca\Desktop\ia-project\Proiect-IA-B4-Modul2\questions_tf.txt","w", encoding = "utf-8-sig")
answer_id_file =  open(r"C:\Users\Alina Coca\Desktop\ia-project\Proiect-IA-B4-Modul2\answers_tf.txt","w", encoding = "utf-8-sig")

#0 - easy, 1 - medium, 2 - hard
#Typpe Values: 2 - TrueOrFalse

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
			if ArticulateWord(first_word) is not None and ArticulateWord(first_word) != "Eroare":
				#print (ArticulateWord(first_word))
				#print (concept_name)
				#print ("-----------")
				rest = concept_name[space_index:] #the  other words in the concept
				question_id += 1
				question = [question_id, inst["domeniu"], 0, "Urmatoarea definitie despre " + ArticulateWord(first_word) + rest + " este adevarata sau falsa?   " + inst["definitie"], 2]	
				question_id_file.write(str(question))
				question_id_file.write("\n")
		else:
			question_id += 1
			question = [question_id, inst["domeniu"], 0, "Urmatoarea definitie despre " + concept_name + " este adevarata sau falsa?   " + inst["definitie"], 2]	
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
			question = [question_id, inst["domeniu"], 0, "Conceptul " + concept_name + " este identic conceptului de " + str(inst["sinonime"][i].lower()), 2]	
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

	concept_name = str(inst["nume"].lower())
	if len(inst["sinonime"]) == 0:

		for inst2 in subjects:

			if len(inst2["sinonime"]) > 0:
				for i in range(0,len(inst2["sinonime"])):
					question_id += 1
					question = [question_id, inst["domeniu"], 0, "Conceptul " + concept_name + " este identic conceptului de " + str(inst2["sinonime"][i].lower()), 2]	
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
