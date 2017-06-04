from .base import CommandBase
from config import METRIKA_OAUTH_APP_ID

class CommandStart(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

        message = "Перейдите по следующей ссылке для авторизации.\n" \
                  "\n" \
                  "https://oauth.yandex.ru/authorize?" \
                  "response_type=code&client_id={}&state={}".format(METRIKA_OAUTH_APP_ID, payload['chat'])

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )
