import requests
import json
# import isodate
from datetime import timedelta
from notion_database.properties import Properties
from notion_database.page import Page


def add_time(tmdlt, time, page_id, token):
    prop = Properties()
    format_time = str(timedelta(seconds=int(time) + int(tmdlt) + 1))
    prop.set_rich_text("Time", format_time)
    prop.set_number("Time_seconds", int(time) + int(tmdlt) + 1)
    # print(time+timedelta+1)
    page = Page(integrations_token=token)
    page.update_page(page_id=page_id, properties=prop)
    return format_time


class Parser:
    def __init__(self, token, database_id='1abc122ef7464fe0ba0612718f635475'):
        self.token = token
        self.database_id = database_id
        self.pages = self.get_pages()
        self.work_pages, self.work_pages_id = self.get_work_pages_id()

    def get_pages(self):
        headers = {'Authorization': self.token,
                   'Notion-Version': '2021-08-16'}
        query = {"sorts": [
            {
                "property": "Order",
                "direction": "ascending"
            }]}
        res = requests.post('https://api.notion.com/v1/databases/' + self.database_id + '/query', headers=headers,
                            data=query)
        # print(self.token)
        pages = [{**page['properties'], **{'id': page['id']}} for page in res.json()['results']]
        return pages

    def get_work_pages_id(self):
        self.pages = self.get_pages()
        self.work_pages = [page for page in self.pages if page['Process']['checkbox'] and not page['Done']['checkbox']]
        self.work_pages_id = [page['id'] for page in self.pages if
                         page['Process']['checkbox'] and not page['Done']['checkbox']]
        return self.work_pages, self.work_pages_id

    def get_time(self):
        time_dict = {}
        for page in self.pages:
            if page['id'] in self.work_pages_id:
                time_dict[page['id']] = page['Time']['rich_text'][0]['text']['content']
        return time_dict

    def update_page_total(self, total_sum):
        total_sum = round(total_sum, 2)
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13"
        }

        update_url = f"https://api.notion.com/v1/blocks/09e380f2-092c-48b3-8f74-affd6c4ffd99"

        update_data = {'heading_1': {'text': [{'type': 'text',
                                               'text': {'content': 'Всего заработано: ', 'link': None},
                                               'annotations': {'bold': False,
                                                               'italic': False,
                                                               'strikethrough': False,
                                                               'underline': False,
                                                               'code': False,
                                                               'color': 'default'},
                                               'plain_text': 'Всего заработано: ',
                                               'href': None},
                                              {'type': 'text',
                                               'text': {'content': str(total_sum) + ' ₽', 'link': None},
                                               'annotations': {'bold': False,
                                                               'italic': True,
                                                               'strikethrough': False,
                                                               'underline': True,
                                                               'code': True,
                                                               'color': 'green'},
                                               'plain_text': str(total_sum) + ' ₽',
                                               'href': None}]}}
        data = json.dumps(update_data)

        response = requests.request("PATCH", update_url, headers=headers, data=data)

    def update_page_today(self, today_sum):
        today_sum = round(today_sum, 2)
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13"
        }

        update_url = f"https://api.notion.com/v1/blocks/0456e753-e42f-4a6e-ae6b-2bf68c7123c1"

        update_data = {'heading_1': {'text': [{'type': 'text',
                                               'text': {'content': 'За сегодня:             ', 'link': None},
                                               'annotations': {'bold': False,
                                                               'italic': False,
                                                               'strikethrough': False,
                                                               'underline': False,
                                                               'code': False,
                                                               'color': 'default'},
                                               'plain_text': 'За сегодня:             ',
                                               'href': None},
                                              {'type': 'text',
                                               'text': {'content': str(today_sum) + ' ₽', 'link': None},
                                               'annotations': {'bold': True,
                                                               'italic': True,
                                                               'strikethrough': False,
                                                               'underline': True,
                                                               'code': True,
                                                               'color': 'green'},
                                               'plain_text': str(today_sum) + ' ₽',
                                               'href': None}]}}
        data = json.dumps(update_data)

        response = requests.request("PATCH", update_url, headers=headers, data=data)
