class CommandBase:

    def __init__(self, sdk):
        self.sdk = sdk

    def get_chat_counters(self, chat):
        return list(self.sdk.db.find('metrika_counters', {'chat_id': chat}))

    def get_access_token(self, user_id):
        try:
            return self.sdk.db.find_one('metrika_tokens', {'user_id': user_id})['access_token']
        except:
            return None