import requests
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard
from typing import List, Dict, Optional, Union, AnyStr


class VKPayloadProcessor:
    def __init__(self, data: dict, vk, peer_id: int):
        self.message = ''
        self.attachments = []
        self.keyboard = None
        self.session = requests.Session()
        self.peer_id = peer_id if peer_id else None

        self.upload = VkUpload(vk)

        if data.get('text'):
            self.message = data['text']
        if data.get('image_url'):
            self.get_image_from_url(data['image_url'])
        if data.get('keyboard'):
            self.parse_keyboard(data['keyboard'])
        if data.get('attachments'):
            self.get_attachments_from_urls(data['attachments'])

    def get_image_from_url(self, url: str):
        f = self.session.get(url, stream=True)
        photo = self.upload.photo_messages(photos=f.raw, peer_id=self.peer_id)[0]
        self.attachments.append(
            f"photo{photo['owner_id']}_{photo['id']}"
        )

    def get_attachments_from_urls(self, urls: List[dict]):
        for file in urls:

            if file.get('vk_id') is not None:
                self.attachments.append(file.get('vk_id'))
                return

            f = self.session.get(file.get('url'), stream=True)

            # TODO really gotta find a way around writing the file to the disk to save it
            with open('/tmp/metadata.' + file.get('extension'), 'wb') as fp:
                for chunk in f.iter_content(chunk_size=8192):
                    fp.write(chunk)

            doc = self.upload.document_message(doc='/tmp/metadata.pdf', title=file.get('title'), peer_id=self.peer_id)['doc']
            self.attachments.append(
                f"doc{doc['owner_id']}_{doc['id']}"
            )

    def parse_keyboard(self, data: Dict):
        self.keyboard = VkKeyboard()
        self.keyboard.one_time = data.get('one_time') or True
        self.keyboard.inline = data.get('inline') or True

        for btn in data.get('buttons'):
            btn = btn[0]
            action_type = btn.get('action').get('type')
            if action_type == 'open_link':
                self.keyboard.add_openlink_button(
                    link=btn.get('action').get('link'),
                    label=btn.get('action').get('label'),
                    payload=btn.get('action').get('payload'),

                )
            elif action_type == 'text':
                self.keyboard.add_button(
                    label=btn.get('action').get('label'),
                    color=btn.get('color')
                )
            else:
                raise NotImplementedError('Unsupported keyboard action type!')

    def get_json_data(self) -> Dict:
        values = {
            'attachment': ','.join(self.attachments) if self.attachments else None,
            'message': self.message,
            'keyboard': self.keyboard.get_keyboard() if self.keyboard else None
        }
        return values


