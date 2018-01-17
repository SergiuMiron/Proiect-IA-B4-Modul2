import json
import sys

def myround(x, base=5):
    return int(base * round(float(x)/base))

with open('fisier1_subiecte.txt', 'r', encoding="utf-8-sig") as data_file:
    json_data_subiecte = data_file.read()

with open('fisier2_proprietati.txt', 'r', encoding="utf-8-sig") as data_file:
    json_data_proprietati = data_file.read()

subjects = json.loads(json_data_subiecte)
properties = json.loads(json_data_proprietati)


dict_domenii = {}
domains = 0
file_domains = open('insert_domains.txt','w', encoding="utf-8-sig")

for inst in subjects:
	if inst['domeniu'] not in dict_domenii.keys():
		domains=domains+1
		dict_domenii[inst['domeniu']] = domains
		query = "INSERT INTO `domains` (id,name) VALUES " + "(" + str(domains) + ", " + '\'' + str(inst['domeniu']) + '\'' + ");"
		file_domains.write(query)
		file_domains.write("\n")

file_domains.close()

file_questions = open('insert_questions.txt','w',encoding="utf-8-sig")

#For matching
with open('matching_q_synonyms.txt','r', encoding="utf-8-sig") as matching_qs:
	for line in matching_qs:
		lista = eval(line)
		if lista[2] == 0:
			diffratio = 1
		elif lista[2] == 1:
			diffratio = 1.3
		else: 
			diffratio=1.8
		secs_to_answer = 0.6 * 90 * diffratio
		secs_to_answer = myround(secs_to_answer)
		query = "INSERT into `questions` (id, domain_id, difficulty, body, question_type, expected_secs_to_answer) VALUES " + "(" + str(lista[0]) + ", " + str(dict_domenii[lista[1]]) + ", " + str(lista[2]) + ", " + "\'" + str(lista[3]) + "\'" +  ", "
		query = query + str(3) + ", " + str(secs_to_answer) + ");\n"
		file_questions.write(query)

with open('matching_q_definition.txt','r', encoding="utf-8-sig") as matching_qs:
	for line in matching_qs:
		lista = eval(line)
		if lista[2] == 0:
			diffratio = 1
		elif lista[2] == 1:
			diffratio = 1.3
		else:
			diffratio = 1.8
		secs_to_answer = 0.6 * 90 * diffratio
		secs_to_answer = myround(secs_to_answer)
		query = "INSERT into `questions` (id, domain_id, difficulty, body, question_type, expected_secs_to_answer) VALUES " + "(" + str(lista[0]) + ", " + str(dict_domenii[lista[1]]) + ", " + str(lista[2]) + ", " + "\'" + str(lista[3]) + "\'" + ", "
		query = query + str(3) + ", " + str(secs_to_answer) + ");\n"
		file_questions.write(query)

with open('matching_q_properties.txt','r', encoding="utf-8-sig") as matching_qs:
	for line in matching_qs:
		lista = eval(line)
		if lista[2] == 0:
			diffratio = 1
		elif lista[2] == 1:
			diffratio = 1.3
		else:
			diffratio = 1.8
		secs_to_answer = 0.6 * 90 * diffratio
		secs_to_answer = myround(secs_to_answer)
		query = "INSERT into `questions` (id, domain_id, difficulty, body, question_type, expected_secs_to_answer) VALUES " + "(" + str(lista[0]) + ", " + str(dict_domenii[lista[1]]) + ", " + str(lista[2]) + ", " + "\'" + str(lista[3])  + "\'" + ", "
		query = query + str(3) + ", " + str(secs_to_answer) + ");\n"
		file_questions.write(query)

#For VM 
with open('questions_vm.txt','r', encoding="utf-8-sig") as vm:
	for line in vm:
		lista = eval(line)
		if lista[2] == 0:
			diffratio = 1
		elif lista[2] == 1:
			diffratio = 1.3
		else:
			diffratio = 1.8
		secs_to_answer = 90 * diffratio
		secs_to_answer = myround(secs_to_answer)
		lista[0] = lista[0] + 1000
		query = "INSERT into `questions` (id, domain_id, difficulty, body, question_type, expected_secs_to_answer) VALUES " + "(" + str(lista[0]) + ", " + str(dict_domenii[lista[1]]) + ", " + str(lista[2]) + ", " + "\'" + str(lista[3])  + "\'" + ", "
		query = query + str(0) + ", " + str(secs_to_answer) + ");\n"
		file_questions.write(query)


#For FillIn
with open('fillin_q_definitions.txt','r', encoding="utf-8-sig") as vm:
	for line in vm:
		lista = eval(line)
		if lista[2] == 0:
			diffratio = 1
		elif lista[2] == 1:
			diffratio = 1.3
		else:
			diffratio = 1.8
		secs_to_answer = 90 * diffratio
		secs_to_answer = myround(secs_to_answer)
		lista[0] = lista[0] + 2000
		query = "INSERT into `questions` (id, domain_id, difficulty, body, question_type, expected_secs_to_answer) VALUES " + "(" + str(lista[0]) + ", " + str(dict_domenii[lista[1]]) + ", " + str(lista[2]) + ", " + "\'" + str(lista[3])  + "\'" + ", "
		query = query + str(1) + ", " + str(secs_to_answer) + ");\n"
		file_questions.write(query)

#Will fix this
'''with open('fillin_q_synonyms.txt','r', encoding="utf-8-sig") as vm:
	for line in vm:
		lista = eval(line)
		if lista[2] == 0:
			diffratio = 1
		elif lista[2] == 1:
			diffratio = 1.3
		else:
			diffratio = 1.8
		secs_to_answer = 90 * diffratio
		secs_to_answer = myround(secs_to_answer)
		lista[0] = lista[0] + 2000
		print(lista)
		query = "INSERT into `questions` (id, domain_id, difficulty, body, question_type, expected_secs_to_answer) VALUES " + "(" + str(lista[0]) + ", " + str(dict_domenii[lista[1]]) + ", " + str(lista[2]) + ", " + "\'" + str(lista[3])  + "\'" + ", "
		query = query + str(3) + ", " + str(secs_to_answer) + ");\n"
		file_questions.write(query)'''


#For True/False
#TODO


file_answers = open('insert_answers.txt','w',encoding="utf-8-sig")

#For matching
with open('matching_a_synonyms.txt','r', encoding="utf-8-sig") as matching_as:
	for line in matching_as:
		lista = eval(line)
		if lista[3] == True or lista[3] == 'True' or lista[3] == 1 or lista[3] == '1':
			OK = 1
		else:
			OK = 0
		query = "INSERT into `answers` (id, question_id, body, is_correct) VALUES " + "(" + str(lista[0]) + ", " + str(lista[1]) + ", " "\'" + str(lista[2]) + "\'" + ", " + str(OK) + ");\n"
		file_answers.write(query)

with open('matching_a_definition.txt','r', encoding="utf-8-sig") as matching_as:
	for line in matching_as:
		lista = eval(line)
		if lista[3] == True or lista[3] == 'True' or lista[3] == 1 or lista[3] == '1':
			OK = 1
		else:
			OK = 0
		query = "INSERT into `answers` (id, question_id, body, is_correct) VALUES " + "(" + str(lista[0]) + ", " + str(lista[1]) + ", " "\'" + str(lista[2]) + "\'" + ", " + str(OK) + ");\n"
		file_answers.write(query)

with open('matching_a_properties.txt','r', encoding="utf-8-sig") as matching_as:
	for line in matching_as:
		lista = eval(line)
		if lista[3] == True or lista[3] == 'True' or lista[3] == 1 or lista[3] == '1':
			OK = 1
		else:
			OK = 0
		query = "INSERT into `answers` (id, question_id, body, is_correct) VALUES " + "(" + str(lista[0]) + ", " + str(lista[1]) + ", " "\'" + str(lista[2]) + "\'" + ", " + str(OK) + ");\n"
		file_answers.write(query)


#For VM
with open('answers_vm.txt','r', encoding="utf-8-sig") as vm:
	for line in vm:
		lista = eval(line)
		if lista[3] == True or lista[3] == 'True' or lista[3] == 1 or lista[3] == '1':
			OK = 1
		else:
			OK = 0
		lista[0] = lista[0] + 1000
		lista[1] = lista[1] + 1000
		query = "INSERT into `answers` (id, question_id, body, is_correct) VALUES " + "(" + str(lista[0]) + ", " + str(lista[1]) + ", " "\'" + str(lista[2]) + "\'" + ", " + str(OK) + ");\n"
		file_answers.write(query)


#For FillIn
with open('fillin_a_definitions.txt','r', encoding="utf-8-sig") as vm:

	for line in vm:
		lista = eval(line)
		if lista[3] == True or lista[3] == 'True' or lista[3] == 1 or lista[3] == '1':
			OK = 1
		else:
			OK = 0
		lista[0] = lista[0] + 2000
		lista[1] = lista[1] + 2000
		query = "INSERT into `answers` (id, question_id, body, is_correct) VALUES " + "(" + str(lista[0]) + ", " + str(lista[1]) + ", " "\'" + str(lista[2]) + "\'" + ", " + str(OK) + ");\n"
		file_answers.write(query)

#Will fix this
'''with open('fillin_a_synonyms.txt','r', encoding="utf-8-sig") as vm:

	for line in vm:
		lista = eval(line)
		if lista[3] == True or lista[3] == 'True' or lista[3] == 1 or lista[3] == '1':
			OK = 1
		else:
			OK = 0
		lista[0] = lista[0] + 2000
		lista[1] = lista[1] + 2000
		query = "INSERT into `answers` (id, question_id, body, is_correct) VALUES " + "(" + str(lista[0]) + ", " + str(lista[1]) + ", " "\'" + str(lista[2]) + "\'" + ", " + str(OK) + ");\n"
		file_answers.write(query)'''

#For True/False
#TODO
file_answers.close()
