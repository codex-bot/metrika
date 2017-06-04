from .base import CommandBase
from config import METRIKA_OAUTH_APP_ID, USERS_COLLECTION_NAME
import random
import string
from time import time

class CommandStart(CommandBase):

    @staticmethod
    def generate_user_token():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

    async def __call__(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

        registered_chat = self.sdk.db.find_one(USERS_COLLECTION_NAME, {'chat': payload['chat']})

        if registered_chat:
            user_token = registered_chat['user']
        else:
            user_token = self.generate_user_token()
            new_chat = {
                'chat': payload['chat'],
                'user': user_token,
                'dt_register': time()
            }
            self.sdk.db.insert(self.USERS_COLLECTION_NAME, new_chat)
            self.sdk.log("New user registered with token {}".format(user_token))

        message = "Перейдите по следующей ссылке для авторизации.\n" \
                  "\n" \
                  "https://oauth.yandex.ru/authorize?" \
                  "response_type=code&client_id={}&state={}".format(METRIKA_OAUTH_APP_ID, user_token)

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )
