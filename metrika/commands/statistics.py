import io

from .base import CommandBase
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pycapella


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

        counters = list(self.sdk.db.find(self.COLLECTIONS['counters'], {'chat_id': payload["chat"]}))

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

        await self.sdk.send_text_to_chat(payload["chat"], message)

        for counter in counters:
            user_data = self.sdk.db.find_one(self.COLLECTIONS['tokens'], {
                'user_id': counter['user_id']
            })

            token = user_data['access_token']

            hits, users, users_day = self.get_stats(counter['counter_id'], token, period)

            await self.sdk.send_text_to_chat(payload["chat"],
                       "{}:\n" \
                       "{} уникальных посетителей\n" \
                       "{} просмотров\n\n".format(counter['counter_name'], int(users), int(hits)))

            if payload['command'] == 'weekly':
                try:
                    url = self.get_graph(users_day)
                    if url:
                        await self.sdk.send_image_to_chat(payload["chat"], url)
                except:
                    pass

    def get_graph(self, users_day):
        now = datetime.now()
        axes_labels = [(now - timedelta(i)).strftime("%d.%m") for i in range(now.weekday(), -1, -1)]
        fig = plt.figure(figsize=(6, 3), dpi=80)
        ax = fig.add_subplot(111)
        ax.plot(axes_labels, np.array(users_day), 'b')
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        try:
            response = pycapella.Capella().upload_file(buf.getvalue(), raw_input=True)
        except:
            return None
        else:
            return response['url']

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
            'date2': 'today',
            'group': 'day'
        }

        statistic = requests.get(self.API_URL, params=params, timeout=5).json()

        hits, users = statistic['totals'][0]
        users_day = statistic['data'][0]['metrics'][1]

        return hits, users,users_day

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
