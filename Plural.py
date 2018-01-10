import urllib.request


def get_plural(word):
    word = word.lower()

    fin_word = word
    fin_word = fin_word.replace("ă", r"%C4%83")
    fin_word = fin_word.replace("î", r"%C3%AE")
    fin_word = fin_word.replace("â", r"%C3%A2")
    fin_word = fin_word.replace("ț", r"%C8%9B")
    fin_word = fin_word.replace("ș", r"%C8%99")

    the_url = "https://dexonline.ro/definitie/" + fin_word + "/paradigma"

    fp = urllib.request.urlopen(the_url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")

    x = mystr.find("nominativ-acuzativ</td>")

    newstr = mystr[x:]

    x = newstr.find("genitiv-dativ")

    newstr2 = newstr[:x]

    newstr2 = newstr2.replace("<span class=\"accented\">", "")
    newstr2 = newstr2.replace("</span>", "")
    newstr2 = newstr2.replace("<tr>", "")
    newstr2 = newstr2.replace("<td>", "")
    newstr2 = newstr2.replace("</td>", "")
    newstr2 = newstr2.replace("</tr>", "")

    list_all_4 = list()

    for i in range(1, 5):
        index = newstr2.find("<td class=\"form\">")
        the_word = ""

        beyond = newstr2[index + 17:]

        for character in beyond:
            if character == "<":
                break

            the_word = the_word + character

        the_word = the_word.replace("\t", "")
        the_word = the_word.replace(" ", "")
        the_word = the_word.replace("\n", "")

        list_all_4.append(the_word)

        newstr2 = newstr2[index + 17:]

    if list_all_4[2] is None:
        return word

    return list_all_4[2]
