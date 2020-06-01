import os
import dialogflow_v2 as dialogflow
import telegram
import logging 
from google.protobuf.json_format import MessageToDict
from app import app

os.environ['GOOGLE_APPLICATION_CREDENTIALS']

class TelegramMessageLogHandler(logging.Handler):
    def emit(self, record):
        telegram_token_information_message = app.config['TELEGRAM_TOKEN_INFORMATION_MESSAGE']
        chat_id_information_message = app.config['CHAT_ID_INFORMATION_MESSAGE']
        log_entry = self.format(record)
        bot_error = telegram.Bot(token=telegram_token_information_message)
        bot_error.send_message(chat_id=chat_id_information_message, text=log_entry)


def detect_intent_texts(project_id: str, session_id: str, text: str, language_code: str) -> dict:
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)
    
    response = session_client.detect_intent(
            session=session, query_input=query_input)

    query_result = MessageToDict(response.query_result)

    return query_result
