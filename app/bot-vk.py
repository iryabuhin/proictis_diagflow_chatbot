import random
import vk_api
import logging 
import time
import os
import telegram
from vk_api.bot_longpoll import VkBotLongPoll, VkBotMessageEvent, VkBotEventType
from.handler_tools import TelegramMessageLogHandler, detect_intent_texts
from dotenv import load_dotenv


def echo_vk_event(event, vk_api):
    user_id = event.user_id
    user_message = event.text
    project_id = os.environ['project_id']
    
    try:
        message = detect_intent_texts(project_id, event.user_id, user_message, 'ru-RU')
        if message is not None:
            print(message)
            vk_api.messages.send(
                user_id=event.user_id,
                message=message,
                random_id=random.randint(1,1000000000)
            )
    except Exception:
        logger.exception("Проблема при получении и отправке сообщений Dialogflow")


if __name__ == "__main__":
    load_dotenv()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    logger.addHandler(TelegramMessageLogHandler())
    # logger.info("Бот запущен")
    
    try:
        vk_community_token = os.environ['vk_community_token']
        vk_session = vk_api.VkApi(token=vk_community_token)
        vk_api = vk_session.get_api()
        longpoll = VkBotLongPoll(vk_session)
        # logger.info('Longpoll запущен')
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and VkBotMessageEvent:
                echo_vk_event(event, vk_api)
                
    except Exception:
        logger.exception('Возникла ошибка в боте ВКонтакте ↓')
