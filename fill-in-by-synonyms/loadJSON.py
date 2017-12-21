import json
import pathlib


def get_concepts():
    json_file_subjects_path = str(pathlib.Path(__file__).parent) + "\\fisier1_subiecte.json"

    with open(json_file_subjects_path, 'r', encoding="utf8") as data_file:
        json_data_subiecte = data_file.read()

    return json.loads(json_data_subiecte)


def get_properties():
    json_file_properties_path = str(pathlib.Path(__file__).parent) + "\\fisier2_proprietati.json"

    with open(json_file_properties_path, 'r', encoding="utf8") as data_file:
        json_data_proprietati = data_file.read()

    return json.loads(json_data_proprietati)