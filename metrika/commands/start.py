from .base import CommandBase
from config import METRIKA_OAUTH_APP_ID


class CommandStart(CommandBase):

    async def __call__(self, payload):
        """
        Documentation: https://tech.yandex.ru/oauth/doc/dg/tasks/get-oauth-token-docpage/
        :param payload:
        :return:
        """
        self.sdk.log("/start handler fired with payload {}".format(payload))

        message = "Для подключения счетчика, вам нужно авторизовать бота." \
                  "Для этого перейдите по ссылке и подтвердите доступ:"

        button = [[{
            'text': 'Авторизовать бота',
            'url': "https://oauth.yandex.ru/authorize?"
                   "response_type=code&client_id={}&state={}|{}".format(METRIKA_OAUTH_APP_ID,
                                                                        payload['chat'],
                                                                        payload["user"]),
            'callback_data': ''
        }]]

        await self.sdk.send_inline_keyboard_to_chat(
            payload["chat"],
            message,
            button
        )
