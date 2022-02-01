from events.base import EventBase
from commands.add_counter import CommandAddCounter
from api import MetrikaAPI


class EventAuth(EventBase):
    """
    Process OAuth Event. Obtain access token and save it to DB.
    1. Get code and state from request.
    2. Send code and get access token from Yandex.
    3. Insert pair (access_toke, chat_id) to DB 'metrika_tokens' if not exists
    4. Build buttons list with counters for the access token.
    5. Send success message
    """

    async def __call__(self, request):
        if 'code' not in request['query']:
            self.sdk.log("Metrika route handler: code is missed")
            return False

        if 'state' not in request['query']:
            self.sdk.log("Metrika route handler: user_token in state is missed")
            return False

        chat_id, user_id = request['query']['state'].split("|")
        code = request['query']['code']

        try:
            access_token_response = MetrikaAPI.get_access_token(code)
            access_token = access_token_response['access_token']
            user_info = MetrikaAPI.get_user(access_token)
        except Exception as e:
            self.sdk.log("Error: {}".format(e))
            return False
        else:
            if not self.sdk.db.find_one(self.COLLECTIONS['counters'], {'access_token': access_token, 'user_id': user_id}):
                self.sdk.db.insert('metrika_tokens', {
                    'access_token': access_token,
                    'user_id': user_id,
                    'user_info': user_info,
                    'chat_id': chat_id
                })

            # Show available counters to the chat
            await CommandAddCounter(self.sdk).list({
                'chat': chat_id,
                'user': user_id
            })

        return True
