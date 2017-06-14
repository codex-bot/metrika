from .base import CommandBase
import requests
from datetime import datetime, timedelta

class CommandStatistics(CommandBase):
    """
    Return statistics for /today, /weekly, /monthly
    """

    API_URL = 'https://api-metrika.yandex.ru/stat/v1/data/bytime'

    async def stats(self, payload):
        """
        Send statistic for each counter in chat

        :param payload:
        :return:
        """


        counters = list(self.sdk.db.find('metrika_counters', {'chat_id': payload["chat"]}))

        if not len(counters):
            return await self.sdk.send_text_to_chat(
                payload["chat"],
                "Не авторизован ни один пользователь\n" \
                "\n" \
                "Для авторизации используйте /metrika_add"
            )

        period = payload['command']

        date = self.get_date()
        now = datetime.now()

        if period == 'weekly':
            period = 'today' if not now.weekday() else '{}daysAgo'.format(now.weekday())
            monday = (now - timedelta(now.weekday())).strftime('%d').zfill(2)
            message = "С понедельника, {} {} по сегодняшний день.\n\n".format(monday,
                                                                          date['month'])
        elif period == 'monthly':
            period = 'today' if not now.day - 1 else '{}daysAgo'.format(now.day - 1)
            message = "Данные за текущий месяц.\n\n"

        else:
            message = "Сегодня {} {}, {}. Данные к {}:{}.\n\n".format(date['day'],
                                                                      date['month'],
                                                                      date['weekday'],
                                                                      date['hour'],
                                                                      date['minute'])

        for counter in counters:
            user_data = self.sdk.db.find_one('metrika_tokens', {
                'user_id': counter['user_id']
            })

            token = user_data['access_token']

            hits, users = self.get_stats(counter['counter_id'], token, period)

            message += "{}:\n" \
                       "{} уникальных посетителей\n" \
                       "{} просмотров\n\n".format(counter['counter_name'], int(users), int(hits))

            await self.sdk.send_text_to_chat(
                payload["chat"],
                message
            )

    def get_stats(self, counter, token, date1):
        """
        Make request to Metrika Api and gets hits and unique users statistic from :param date1: to today

        :param counter: counter id
        :param token: OAuth token of counter owner
        :param date1: start of statistic period
        :return:
        """

        params = {
            'id': counter,
            'oauth_token': token,
            'metrics': 'ym:s:pageviews,ym:s:users',
            'date1': date1,
            'date2': 'today'
        }

        statistic = requests.get(self.API_URL, params=params, timeout=5).json()

        hits, users = statistic['totals'][0]
        return hits, users

    @staticmethod
    def get_date():

        time = datetime.now()

        def week(n):
            days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
            return days[n]

        def month(n):
            months = [None, 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                    'июля', 'августа', 'сентярбя', 'октября', 'ноября', 'декабря']
            return months[n]

        return {
            'minute': str(time.minute).zfill(2),
            'hour': str(time.hour).zfill(2),
            'day': str(time.day).zfill(2),
            'month': month(time.month),
            'weekday': week(time.weekday()),
        }