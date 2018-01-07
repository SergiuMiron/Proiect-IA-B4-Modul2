import loadJSON
import articulation
import pathlib
import difficulty
import word_gender
import plural


def remove_duplicates(concepte):
    lista = list()
    nume = set()
    try:
        for dictionar in concepte:
            for key, value in dictionar.items():
                if key == "nume":
                    nume.add(value)
        for n in nume:
            for c in concepte:
                if n == c["nume"]:
                    lista.append(c)
                    break
        return lista
    except IndexError as e:
        print("Eroare: " + str(e))


class Answer:
    id = 0

    def __init__(self):
        self.id = 0
        self.qid = 0
        self.statement = []
        self.valid = True


class Question:
    id = 0

    def __init__(self):
        self.id = 0
        self.statement = ""
        self.field = -1
        self.type = 1


class Field:
    id = 0
    all_fields = []

    def __init__(self):
        self.id = -1
        self.nume = ""


def has_synonyms(concept):

    if len(concept["sinonime"]) > 0:
        return True
    else:
        return False


def create_question(concept_p):

    print(concept_p["nume"])

    question = Question()
    Question.id += 1
    # Avem variabila statica ce retine id-ul intrebarii, dar avem si variabila de instanta ca sa stim pe viitor id-ul acesteia.
    question.id = Question.id

    # q_a_f -> Lista in care retinem intrebarea, raspunsurile si domeniul
    q_a_f = []
    questions = []
    answers = []
    fields = []

    field = Field()
    field.nume = concept_p["domeniu"]

    # Luam domeniul din obiectul json si vedem daca exista deja in lista tuturor domeniilor.
    # Daca exista, il copiem id-ul sau.
    for fld in Field.all_fields:
        if field.nume == fld.nume:
            field.id = fld.id
            break

    # Retinem domeniul in lista statica "all_fields"  in cazul in care este unul nou.
    if field.id == -1:
        Field.id += 1
        field.id = Field.id
        Field.all_fields.append(field)
        fields.append(field)

    question.field = field.id

    # Extragem cuvintele
    words_q = concept_p["nume"].split(' ')
    first_word = words_q[0].lower()
    gender = word_gender.get_gender(first_word)
    first_word_articulated = str(articulation.articulate_word(first_word)).capitalize()
    word_plural = plural.get_plural(first_word)

    question.statement = str(first_word_articulated) + ' '

    # In cazul in care avem mai multe cuvinte in numele conceptului, articulam doar primul cuvant si ii facem prima litera majuscula.
    if len(words_q) > 1:
        for index in range(1, len(words_q)):
            question.statement = question.statement + words_q[index] + ' '

    if gender == 'feminin':
        # Forma de feminin singular/plural
        if word_plural != first_word:
            question.statement = question.statement + "mai este cunoscută și sub numele de"
        else:
            question.statement = question.statement + "mai sunt cunoscute și sub numele de"
    elif gender == "masculin":
        # Forma de masculin singular/plural
        if word_plural != first_word:
            question.statement = question.statement + "mai este cunoscut și sub numele de"
        else:
            question.statement = question.statement + "mai sunt cunoscuți și sub numele de"
    else:
        # Forma de neutru singular/plural
        if word_plural != first_word:
            question.statement = question.statement + "mai este cunoscut și sub numele de"
        else:
            question.statement = question.statement + "mai sunt cunoscute și sub numele de"

    questions.append(question)

    # Pentru fiecare sinonim am un alt raspuns.
    for sinonim in concept_p["sinonime"]:
        answer = Answer()
        Answer.id += 1
        answer.id = Answer.id
        answer.qid = question.id
        answer.statement.append(sinonim)
        answers.append(answer)

    q_a_f.append(questions)
    q_a_f.append(answers)
    q_a_f.append(fields)

    return q_a_f


concepts = loadJSON.get_concepts()
properties = loadJSON.get_properties()

# Elimin duplicatele. La mine, de exemplu,
# apare de mai multe ori conceptul de Perete anterior (si posterior si superior etc)..
result = remove_duplicates(concepts)

answers_file = open(str(pathlib.Path(__file__).parent) + "\\answers.txt", "w", encoding="utf8")
questions_file = open(str(pathlib.Path(__file__).parent) + "\\questions.txt", "w", encoding="utf8")
fields_file = open(str(pathlib.Path(__file__).parent) + "\\fields.txt", "w", encoding="utf8")

for cpt in result:
    if has_synonyms(cpt):
        qst_answ_field = create_question(cpt)

        for raspuns in qst_answ_field[1]:
            answer_difficulty = difficulty.diffBasedOnNodeDist(cpt["id"], raspuns.id)
            questions_file.write(str(qst_answ_field[0][0].id) + ",  " + str(qst_answ_field[0][0].field) + ",  " + str(answer_difficulty) + ",  " + qst_answ_field[0][0].statement + ",  " + str(qst_answ_field[0][0].type) + '\n')
            answers_file.write(str(raspuns.id) + ",  " + str(raspuns.qid) + ",  " + raspuns.statement[0] + ",  " + str(raspuns.valid) + '\n')

        if len(qst_answ_field[2]) > 0:
            fields_file.write(str(qst_answ_field[2][0].id) + ",  " + qst_answ_field[2][0].nume + '\n')