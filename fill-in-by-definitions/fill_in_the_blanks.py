import json
import random
import pathlib
from Articulation import ArticulateWord
from Dificulty import diffBasedOnNodeDist


def get_data_from_json(filename):
    try:
        file = open(str(pathlib.Path(__file__).parent) + "\\" + filename, "r", encoding="utf-8-sig")
        to_return = json.loads(file.read())
        return to_return
    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Cannot open file")
    except Exception as e:
        print(e)


def fill_in_by_def(nr_questions):
    try:
        subjects = get_data_from_json("fisier1_subiecte.json")
        nr_questions = min(int(nr_questions), len(subjects))
        random.shuffle(subjects)

        answers_file = open(str(pathlib.Path(__file__).parent) + "\\answers.txt", "w", encoding="utf-8-sig")
        questions_file = open(str(pathlib.Path(__file__).parent) + "\\questions.txt", "w", encoding="utf-8-sig")

        answer_id = 0
        question_id = 0

        for inst in subjects:
            if "este" in inst["definitie"] or "Este" in inst["definitie"]:
                answer_data = inst["nume"]
                question_data = str.lower(inst["definitie"])
                if inst["definitie"].startswith("Este"):
                    question_data_final = question_data
                else:
                    index_space = question_data.index("este")
                    question_data_final = question_data[index_space:]

                if answer_data.count(" ") == 0:
                    answer_data_final = ArticulateWord(answer_data).capitalize()
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id + 1, answer_data_final, True]
                    answers_file.write(str(answer) + '\n')
                else:
                    index_space = answer_data.index(" ")
                    first_word = answer_data[0:index_space]
                    answer_data_final = ArticulateWord(str.lower(first_word)).capitalize() + answer_data[index_space:]
                    answer_id = answer_id + 1
                    answer = [answer_id, question_id + 1, answer_data_final, True]
                    answers_file.write(str(answer) + '\n')

                # Daca am putut construi un raspuns valid adaugam si intrebarea
                if question_id < answer_id:
                    question_id = question_id + 1
                    # al 3-lea argument este dificultatea: 0 - easy, 1 - medium, 2 - hard
                    question = [question_id, inst["domeniu"], diffBasedOnNodeDist(inst["id"]), "... " + question_data_final, "FillIn"]
                    questions_file.write(str(question) + '\n')
                    nr_questions = nr_questions - 1

                if nr_questions == 0:
                    break

        answers_file.close()
        questions_file.close()

    except FileNotFoundError:
        print("File not found")
    except IOError:
        print("Cannot open file")
    except ValueError:
        print("Wrong data type for nr of questions")
    except Exception as e:
        print(e)


fill_in_by_def(30)

