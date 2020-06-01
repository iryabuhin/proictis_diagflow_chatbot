import vk_api
from vk_api.utils import get_random_id
from singleton_decorator import singleton
from app import app


@singleton
class VkAPI_:
    """Singleton VK API interaction class. User self.group_api to call methods requiring group auth,
     self.app_api for everything else"""

    def __init__(self, app_token: str, group_token: str, app_id: int, client_secret: str):
        print('VK API singleton constructor called')
        self.app_token = app_token
        self.app_id = app_id
        self.client_secret = client_secret
        self.group_token = group_token

        # App auth session with App Credentials Flow
        session = vk_api.VkApi(
            token=self.app_token,
            app_id=self.app_id,
            client_secret=self.client_secret,
            api_version='5.90'
        )

        self.app_api = session.get_api()
        # Regular group auth session
        session_ = vk_api.VkApi(token=self.group_token, api_version='5.90')
        self.group_api = session_.get_api()

    def send_msg_from_group(self, peer_id: int, message: str, attachment=None,
                            keyboard=None, dont_parse_links=0):
        if message is None and attachment is None:
            raise vk_api.VkApiError('No message or attachment provided')

        self.group_api.messages.send(
            peer_id=peer_id,
            message=message,
            attachment=attachment,
            keyboard=keyboard,
            dont_parse_links=dont_parse_links,
            random_id=get_random_id()
        )


vk = VkAPI_(
    app_token=app.config['VK_APP_SERVICE_KEY'],
    app_id=app.config['VK_APP_ID'],
    group_token=app.config['VK_COMMUNITY_TOKEN'],
    client_secret=app.config['VK_APP_CLIENT_SECRET']
)