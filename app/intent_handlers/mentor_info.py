from pydialogflow_fulfillment import DialogflowRequest
from flask import jsonify, make_response
from fuzzywuzzy import process, fuzz
import json
import os.path

def get_mentor_info(req: DialogflowRequest):
    q = req.get_parameter('mentor_name')

    json_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'proictis_mentors_api.json')

    # TODO change all this stuff below to query the database instead of a json file
    with open(json_path, 'r') as fp:
        d = json.load(fp)

    best_match = process.extractOne(
        query=q, scorer=fuzz.ratio, processor=str.lower,
        choices=[mentor['surname'] for mentor in d['items']],
        score_cutoff=80
    )

    if best_match is None:
        return jsonify({"fulfillmentText": f'Извините, я не знаю наставника с фамилией {q}.'})

    best_match = best_match[0]
    index = 0
    for i, mentor in enumerate(d['items']):
        if best_match.split()[0] == mentor['surname']:
            index = i
            break

    m = d['items'][index]

    response_text = list()
    response_text.append(f"{' '.join([m['surname'], m['name'], m['patronymic']])} - {m['post'].lower()}")
    response_text.append(m['directions']+'\n')
    response_text.append('Электронная почта: ' + m['email'])

    response_text = '\n'.join(response_text)

    resp = {
        "fulfillmentText": response_text,
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [response_text]
                }
            }
        ]
    }

    vk_payload = {
        "text": response_text,
        "image_url": m['avatar']['link'],
        "attachments": [
            {
                "url": m['files'][0]['link'],
                "title": 'Информация о наставнике',
                "extension": "pdf"
            }
        ],
        "keyboard": {
            "inline": False,
            "one_time": True,
            "buttons": [
                [
                    {
                        "action": {
                            "type": "open_link",
                            "link": "https://proictis.sfedu.ru/mentors",
                            "label": "Информация о других наставниках"
                        }
                    }
                ]
            ]
        }
    }

    resp['payload'] = {'vk': vk_payload}
    return jsonify(resp)

