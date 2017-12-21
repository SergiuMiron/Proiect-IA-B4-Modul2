import json



#TODO - CHECK FOR DUPLICATES IN QUESTIONS/ANSWERS - FIND A WAY TO MEASURE DIFFICULTY - MATCH BY SPLITTING THE DEFINITIONS OF A SUBJECT IN TWO


#Change path
with open(r'C:\Users\Vlad\Desktop\fisier1_subiecte.txt',  'r' , encoding = "utf8") as data_file:
    json_data_subiecte = data_file.read()

with open(r'C:\Users\Vlad\Desktop\fisier2_proprietati.txt', 'r' , encoding = "utf8") as data_file:
    json_data_proprietati = data_file.read()

subjects = json.loads(json_data_subiecte)
properties = json.loads(json_data_proprietati)



#O sa avem o lista de dictionare ( 1 dictionar = 1 json / o instanta )
print(type(subjects))
print(type(properties))


question_id = 0
answer_id = 0

#Create files for testing question_id / answer_id

question_id_file = open(r'C:\Users\Vlad\Desktop\ProjectIA\questions_synonyms.txt','w', encoding = "utf8")
answer_id_file =  open(r'C:\Users\Vlad\Desktop\ProjectIA\answers_synonyms.txt','w', encoding = "utf8")


#Match by synonyms
for inst in subjects:
	if inst["sinonime"] != []:
		question_id = question_id + 1
		question = [question_id,inst["domeniu"],"Easy",inst["nume"],"SingleMatch"]
		#print(inst["nume"])

		question_id_file.write(str(question))
		question_id_file.write("\n")
		x = inst["sinonime"]
		#print(x)

		for sinonim in x:
			answer_id = answer_id+1;
			answer = [answer_id,question_id,sinonim,"True"]
			answer_id_file.write(str(answer))
			answer_id_file.write("\n")


		#print("\n\n\n")


question_id_file.close()
answer_id_file.close()

question_id_file = open(r'C:\Users\Vlad\Desktop\ProjectIA\questions_properties.txt','w', encoding = "utf8")
answer_id_file =  open(r'C:\Users\Vlad\Desktop\ProjectIA\answers_properties.txt','w', encoding = "utf8")

#Match by properties
for inst in properties:
	if inst["id_sub"] != []:
		for id_subiect in inst["id_sub"]:
			#print(id_subiect)
			x = [i for i in subjects if i["id"] == id_subiect]
			if x != []:
				x = x[0]
				question_id = question_id + 1
				question = [question_id,x["domeniu"],"Easy",x["nume"],"SingleMatch"]

				answer_id = answer_id + 1
				answer = [answer_id,question_id,inst["nume"],"True"]

				question_id_file.write(str(question)+"\n")
				answer_id_file.write(str(answer)+"\n")


question_id_file.close()
answer_id_file.close()



#Match by splitting the definitions of a subject - TODO



