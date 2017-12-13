import json


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

#Iterare prin instante
for inst in subjects:
	print(inst,"\n\n")

for inst in properties:
	print(inst,"\n\n")


#Al 4-lea element
print(subjects[3])
print(subjects[3]["id"])
print(subjects[3]["nume"])
print(subjects[3]["sinonime"])

print(properties[3])
print(properties[3]["id"])
print(properties[3]["nume"])

