

#TODO - Not sure how to work around for diacritics

def ArticulateWord(word):

	print("Before art:",word)

	try:
		import urllib.request

		the_url = "https://dexonline.ro/definitie/" + word + "/paradigma"

		fp = urllib.request.urlopen(the_url)
		mybytes = fp.read()

		mystr = mybytes.decode("utf8")
		fp.close()


		x = mystr.find("nominativ-acuzativ</td>")

		newstr = mystr[x:]

		x = newstr.find("genitiv-dativ")

		newstr2 = newstr[:x]

		newstr2 = newstr2.replace("<span class=\"accented\">","")
		newstr2 = newstr2.replace("</span>","")
		newstr2 = newstr2.replace("<tr>","")
		newstr2 = newstr2.replace("<td>","")
		newstr2 = newstr2.replace("</td>","")
		newstr2 = newstr2.replace("</tr>","")

		list_all_4 = list()

		for i in range(1,5):
			index = newstr2.find("<td class=\"form\">")
			the_word = ""

			beyond = newstr2[index+17:]

			for character in beyond:
				if character == "<":
					break

				the_word = the_word + character

			the_word = the_word.replace("\t","")
			the_word = the_word.replace(" ","")
			the_word = the_word.replace("\n","")

			#print(len(the_word))
			#print(the_word)

			list_all_4.append(the_word)

			newstr2 = newstr2[index+17:]

		if word == list_all_4[0]:
			return list_all_4[1]

		if word == list_all_4[1]:
			return list_all_4[1];

		if word == list_all_4[2]:
			return list_all_4[3]

		if word == list_all_4[3]:
			return list_all_4[3]
	except:
		return "Eroare"


data = "fibră"

print(ArticulateWord("cutie"))
print(ArticulateWord(data))
print(ArticulateWord("cutiile"))
print(ArticulateWord("paralel"))