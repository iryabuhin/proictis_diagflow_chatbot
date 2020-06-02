from flask import request, jsonify, make_response
from pydialogflow_fulfillment import DialogflowRequest
from app import app, db
from app.vk_middleware import VKPayloadProcessor
from app.handler_tools import detect_intent_texts
from app import vk
from app.intent_handler_dict import INTENT_HANDLER


@app.route('/webhook', methods=['POST'])
def processing():
    req = DialogflowRequest(request.data)
    data = request.get_json(silent=True, force=True)

    intent_name = req.get_intent_displayName()

    try:
        return INTENT_HANDLER[intent_name](req)
    except KeyError:
        return ''


@app.route('/callback', methods=['POST'])
def process_vk():
    data = request.get_json(force=True, silent=True)

    if not data or 'type' not in data:
        return 'Bad request'
    elif data.get('type') == 'confirmation':
        return app.config['VK_CONFIRMATION']
    elif data.get('type') == 'message_new':
        message = data.get('object').get('text')
        peer_id = data.get('object').get('peer_id')

        query_result = detect_intent_texts(
            app.config['PROJECT_ID'],
            peer_id,
            message,
            'ru-RU'
        )

        # if custom VK payload is present, process it
        # otherwise return fulfillment text
        if query_result.get('webhookPayload'):
            if query_result.get('webhookPayload').get('vk'):
                m = VKPayloadProcessor(
                    data=query_result['webhookPayload']['vk'],
                    vk=vk.group_api,
                    peer_id=peer_id
                )
                response = m.get_json_data()
                vk.send_msg_from_group(peer_id=peer_id, **response)
        else:
            vk.send_msg_from_group(
                peer_id=peer_id,
                message=query_result.get('fulfillmentText')
            )

        return 'ok'


@app.cli.command('initdb')
def init_db():
    db.create_all()


@app.cli.command('resetdb')
def reset_db():
    db.drop_all()
