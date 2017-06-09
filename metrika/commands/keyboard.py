import json

import requests

from config import METRIKA_OAUTH_APP_ID, METRIKA_OAUTH_APP_SECRET
from .base import CommandBase


class CommandInlineKeyboard(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("Inline keyboard handler fired with payload {}".format(payload))

        try:
            method, inline_params = payload['data'].split('|')
            chat_id = payload['chat']
            user_id = payload['user']

            if method == 'add_counter':
                # Expect payload be string(counter id)
                counter_id = inline_params
                oauth_token = self.get_oauth_token(user_id)
                counter_name = self.get_counter_name(counter_id, oauth_token)

                if self.sdk.db.find_one('metrika_counters', {'chat_id': chat_id, 'counter_id': counter_id}):
                    await self.sdk.send_text_to_chat(
                        payload["chat"],
                        'Счетчик *{}* уже прикреплен к данному чату.'.format(counter_name),
                        'Markdown'
                    )
                else:
                    self.sdk.db.insert('metrika_counters', {
                        'chat_id': chat_id,
                        'counter_id': counter_id,
                        'user_id': user_id
                    })
                    await self.sdk.send_text_to_chat(
                        payload["chat"],
                        'Готово! Счетчик *{}* успешно прикреплен к данному чату.'.format(counter_name),
                        'Markdown'
                    )
        except Exception as e:
            self.sdk.log("Error: {}".format(e))

    @staticmethod
    def get_counter_name(id, oauth_token):
        """
        Return counter name by id.
        Documentation: https://tech.yandex.ru/metrika/doc/api2/management/counters/counter-docpage/
        :param code: string
        :return: counter_name (JSON)
        """
        url = 'https://api-metrika.yandex.ru/management/v1/counter/{}?oauth_token={}'.format(id, oauth_token)
        # TODO: change requests to aiohttp
        r = requests.get(url=url)
        return r.json()['counter']['name']

    def get_oauth_token(self, user_id):
        try:
            return self.sdk.db.find_one('metrika_tokens', {'user_id': user_id})['access_token']
        except:
            return None
