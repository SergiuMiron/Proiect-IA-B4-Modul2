def WordGender(word):
	try:
		import urllib.request

		word = word.lower()

		#print(word)

		fin_word = word
		fin_word = fin_word.replace("ă",r"%C4%83")
		fin_word = fin_word.replace("î",r"%C3%AE")
		fin_word = fin_word.replace("â",r"%C3%A2")
		fin_word = fin_word.replace("ț",r"%C8%9B")
		fin_word = fin_word.replace("ș",r"%C8%99")

		the_url = "https://dexonline.ro/definitie/" + fin_word + "/paradigma"

		fp = urllib.request.urlopen(the_url)
		mybytes = fp.read()

		mystr = mybytes.decode("utf8")
		fp.close()

		neutru = mystr.find("/eticheta.php?id=52")
		feminin = mystr.find("/eticheta.php?id=51")
		masculin = mystr.find("/eticheta.php?id=50")

		if neutru == -1 and feminin == -1 and masculin == -1:
			return "Unknown"

		if neutru == -1:
			neutru = 999999999999
		if feminin == -1:
			feminin = 999999999999
		if masculin == -1:
			masculin = 999999999999

		#print(neutru,feminin,masculin)

		if neutru < masculin and neutru < feminin:
			return "neutru"

		if masculin < neutru and masculin < feminin:
			return "masculin"

		if feminin < neutru and feminin < masculin:
			return "feminin"

	except Exception as e:
		print(e)



'''print(WordGender("cutie"))
print(WordGender("fibră"))
print(WordGender("cutiile"))
print(WordGender("paralel"))
print(WordGender("spațiu"))
print(WordGender("sânge"))
print(WordGender("BĂRBAT"))
print(WordGender("CUTIa"))
print(WordGender("asad"))'''