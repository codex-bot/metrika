from .base import CommandBase
from config import METRIKA_OAUTH_APP_ID
import random
import string


class CommandStart(CommandBase):

    @staticmethod
    def generate_user_token():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

    async def __call__(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

        message = "Для подключения счетчика, вам нужно авторизовать бота." \
                  "Для этого перейдите по ссылке и подтвердите доступ:\n" \
                  "\n" \
                  "https://oauth.yandex.ru/authorize?" \
                  "response_type=code&client_id={}&state={}".format(METRIKA_OAUTH_APP_ID, payload["chat"])

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )
