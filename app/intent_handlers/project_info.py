from pydialogflow_fulfillment import DialogflowRequest
from flask import jsonify, make_response
from fuzzywuzzy import process, fuzz
import json
import os
from app import url_shortener

folder_path = os.path.abspath(os.path.dirname(__file__))

def get_project_info(req: DialogflowRequest):
    project_name = req.get_parameter('projects')

    with open(os.path.join(folder_path, 'projects.json'), 'r') as fp:
        d = json.load(fp)

    best_match = process.extractOne(
        query=project_name,
        processor=str.lower,
        choices=d.keys(),
        score_cutoff=75,
        scorer=fuzz.token_sort_ratio
    )

    if best_match is None:
        return jsonify({"fulfillmentText": 'Извините, не могу найти информацию '
                                           'о проекте с таким названием.'})
    best_match = best_match[0]
    vk_doc_id = d.get(best_match)

    response_text = 'Вот что мне удалось найти.'
    resp = {"fulfillmentText": response_text, "fulfillmentMessages": [
        {
            "text": {
                "text": [response_text]
            }
        }
    ], 'payload': {
        'vk': {
            'text': response_text,
            'attachments': [{'vk_id': vk_doc_id}],
            "keyboard": {
                "inline": True,
                "one_time": True,
                "buttons": [
                    [
                        {
                            "action": {
                                "type": "open_link",
                                "link": "https://proictis.sfedu.ru/projects",
                                "label": "Больше информации о творческих проектах"
                            }
                        }
                    ]
                ]
        }
        }
    }}

    return jsonify(resp)


def call_followup_event(*args, **kwargs):
    return jsonify({"followupEventInput": {
        "name": "get_all_projects_event",
        "languageCode": "ru-RU"
    }})


def get_all_projects_info(*args, **kwargs):

    text = 'Информацию о всех доступных на данный момент проектах для первого и второго' \
            'курсов можно найти на сайте Проектного офиса: https://proictis.sfedu.ru/projects'

    resp = {
        'payload': {
            'vk': {
                "text": text,
                "image_url": 'https://proictis.sfedu.ru/assets/images/logo_proictis_1.png'
            }
        }
    }

    return jsonify(resp)
