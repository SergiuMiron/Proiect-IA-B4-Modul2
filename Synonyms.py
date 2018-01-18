#calea= "C:\Users\Ioana\Desktop\medicina"
def sinonime_vm( calea):

    import json
    import random
    with open(calea+r'\fisier1_subiecte.txt',  'r' , encoding = "utf-8-sig") as data_file:
        json_data_subiecte = data_file.read()
    with open(calea+r'\fisier2_proprietati.txt', 'r' , encoding = "utf-8-sig") as data_file:
        json_data_proprietati = data_file.read()
    subjects = json.loads(json_data_subiecte)
    properties = json.loads(json_data_proprietati)
    question_id = 0
    answer_id = 0
    nr_sinonime=0
    for inst in subjects:
        if len(inst["sinonime"])>0:
            nr_sinonime=nr_sinonime+1
   # print(nr_sinonime)

    question_id_file = open(calea+r'\intrebari_sinonime_vm.txt', 'w', encoding="utf8")
    answer_id_file = open(calea+r'\raspunsuri_sinonime_vm.txt', 'w', encoding="utf8")

    for inst in subjects:
        if len(inst["sinonime"])>0:
                question_id = question_id + 1
                question = [question_id,[question_id,question_id+nr_sinonime,question_id+nr_sinonime+nr_sinonime],inst["domeniu"],"0","Care dintre urmatoarele variante poate fi sinonim pentru termenul: " + inst["nume"],"0"]
                question_domeniu=inst["domeniu"]
                question_id_file.write(str(question))
                question_id_file.write("\n")
                bool = True
                nr_raspunsuri_totale = 0
                for sinonim in inst["sinonime"]:
                    nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id, sinonim, bool]
                    answer_id_file.write(str(answer))
                    answer_id_file.write("\n")
                    if nr_raspunsuri_totale == 4:
                        break
                y=[]
                while (nr_raspunsuri_totale <= 3):
                    bool = False
                    x = [i for i in subjects if i["sinonime"] != inst["sinonime"] and len(i["sinonime"])>0 and inst["domeniu"]==i["domeniu"]]
                    random.shuffle(x)
                    if x != None:
                        x = x[0]
                        for invalid in x["sinonime"]:
                             if invalid not in y:
                            #    print("dublura in set 2:\n")
                            #    for p in y:
                            #        print(p)
                            # else:
                            # x.pop(invalid,'')
                                nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                                answer_id = answer_id + 1
                                answer = [answer_id, question_id, invalid, bool]
                                answer_id_file.write(str(answer))
                                answer_id_file.write("\n")
                                if nr_raspunsuri_totale == 4:
                                    break
                                y.append(invalid)
                        # for p in y:
                        #    print(p)
    #print("\n\n\nsetul 2")


    for inst in subjects:
        if len(inst["sinonime"])>0:
                question_id = question_id + 1
                question = [question_id,[question_id-nr_sinonime,question_id,question_id+nr_sinonime],inst["domeniu"],"1","Care dintre urmatoarele variante poate fi sinonim pentru termenul: " + inst["nume"],"0"]
                question_domeniu=inst["domeniu"]
                question_id_file.write(str(question))
                question_id_file.write("\n")
                bool = True
                nr_raspunsuri_totale = 0
                sinonim=[]
                for sinonim in inst["sinonime"]:
                    nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id, sinonim, bool]
                    answer_id_file.write(str(answer))
                    answer_id_file.write("\n")
                    if nr_raspunsuri_totale == 4:
                        break
                y=[]
                while (nr_raspunsuri_totale <= 3):
                    bool = False
                    x = [i for i in subjects if i["sinonime"] != inst["sinonime"] and len(i["sinonime"])>0 ]
                    random.shuffle(x)
                    if x!=None :
                        x= x[0]
                        for invalid in x["sinonime"]:
                            if invalid not in y:
                                #print("dublura in set 2:\n")
                                #print("intrebarea numarul: ", question_id)
                                #for p in y:
                                #    print(p)
                            #else:
                                #x.pop(invalid,'')
                                nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                                answer_id = answer_id + 1
                                answer = [answer_id, question_id, invalid, bool]
                                answer_id_file.write(str(answer))
                                answer_id_file.write("\n")
                                if nr_raspunsuri_totale == 4:
                                    break
                                y.append(invalid)
                           # for p in y:
                            #    print(p)
    #print("\n\n\nsetul 3")

    for inst in subjects:
        if len(inst["sinonime"])>0:
                question_id = question_id + 1
                question = [question_id,[question_id-nr_sinonime-nr_sinonime,question_id-nr_sinonime,question_id],inst["domeniu"],"2","Care dintre urmatoarele variante poate fi sinonim pentru termenul: " + inst["nume"],"0"]
                question_domeniu=inst["domeniu"]
                question_id_file.write(str(question))
                question_id_file.write("\n")
                bool = False
                nr_raspunsuri_totale = 0
                voc = ['a', 'ă', 'î', 'â', 'e', 'i', 'o', 'u']
                for sinonim in inst["sinonime"]:
                    nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                    answer_id = answer_id + 1
                    sinonim = sinonim[::-1]
                    for i in sinonim:
                        if i in voc:
                            random.shuffle(voc)
                            if i != voc[0]:
                                sinonim = sinonim.replace(i, voc[0], 1)
                                break
                    sinonim = sinonim[::-1]
                    answer = [answer_id, question_id, sinonim, bool]
                    answer_id_file.write(str(answer))
                    answer_id_file.write("\n")
                    if nr_raspunsuri_totale == 4:
                        break
                y=[]
                while (nr_raspunsuri_totale <= 3):
                    x = [i for i in subjects if i["sinonime"] != inst["sinonime"] and len(i["sinonime"])>0 ]
                    random.shuffle(x)
                    if x!=None :
                        x= x[0]
                        #y
                        for invalid in x["sinonime"]:
                            if invalid not in y:
                               # print("dublura in set 3: \n")
                              #  print("intrebarea numarul: ", question_id)
                             #   for p in y:
                             #        print(p)
                            #else:
                                nr_raspunsuri_totale = nr_raspunsuri_totale + 1
                                answer_id = answer_id + 1
                                answer = [answer_id, question_id, invalid, bool]
                                answer_id_file.write(str(answer))
                                answer_id_file.write("\n")
                                if nr_raspunsuri_totale == 4:
                                    break
                            y.append(invalid)
                            #for p in y:
                                #print(p)

    question_id_file.close()
    answer_id_file.close()
    return nr_sinonime*3

folder=r'C:\Users\Ioana\Desktop\medicina'
print(sinonime_vm(folder))