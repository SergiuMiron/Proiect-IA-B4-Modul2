import loadJSON
import articulation
import pathlib


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
        self.difficulty = ""
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


def get_gender(word):
    if word[-1] == 'ă':
        return 'f'
    else:
        return 'm'


def create_question(concept_p):

    # q_a_f -> Lista in care retinem intrebarea, raspunsul si domeniul
    q_a_f = []

    field = Field()
    field.nume = concept_p["domeniu"]

    question = Question()

    Question.id += 1
    question.id = Question.id

    # In cazul in care avem mai multe cuvinte in numele conceptului articulam doar primul cuvant.
    words_q = concept_p["nume"].split(' ')
    first_word = words_q[0]
    gender = get_gender(first_word)
    first_word_articulated = articulation.articulate_word(first_word)

    if len(words_q) > 1:
        second_word = words_q[1]
        question.statement = first_word_articulated.capitalize() + ' ' + second_word
    else:
        question.statement = first_word_articulated.capitalize()

    if gender == 'f':
        question.statement = question.statement + " mai este cunoscută și sub numele de"
    else:
        question.statement = question.statement + " mai este cunoscut și sub numele de"

    for fld in Field.all_fields:
        if field.nume == fld.nume:
            field.id = fld.id
            break

    # Retinem domeniul in cazul in care este unul nou.
    if field.id == -1:
        Field.id += 1
        field.id = Field.id
        Field.all_fields.append(field)
        q_a_f.append(field)

    question.field = field.id

    q_a_f.insert(0, question)

    # Pentru fiecare sinonim am un alt raspuns.
    for sinonim in concept_p["sinonime"]:
        answer = Answer()
        Answer.id += 1
        answer.id = Answer.id
        answer.qid = question.id
        answer.statement.append(sinonim)
        q_a_f.insert(1, answer)

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
        q = qst_answ_field[0]
        a = qst_answ_field[1]

        questions_file.write(str(q.id) + ",  " + str(q.field) + ",  " + q.difficulty + ",  " + q.statement + ",  " + str(q.type) + '\n')
        answers_file.write(str(a.id) + ",  " + str(a.qid) + ",  " + a.statement[0] + ",  " + str(a.valid) + '\n')

        if len(qst_answ_field) > 2:
            f = qst_answ_field[2]
            fields_file.write(str(f.id) + ",  " + f.nume + '\n')
