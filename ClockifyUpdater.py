from clockifyclient.api import APIServer
from clockifyclient.client import APISession
from pytz import timezone
from datetime import datetime
import requests


class ClockifyUpdater:
    def __init__(self, api_key,
                 workspace_id, user_id,
                 zone=timezone('Europe/Moscow'),
                 ):
        self.api_key = api_key
        self.headers = {'x-api-key': api_key}
        self.workspace_id = workspace_id
        self.user_id = user_id
        self.zone = zone
        self.session = APISession(
            api_server=APIServer("https://api.clockify.me/api/v1"), api_key=api_key)
        if self.session.get_projects():
            self.project = self.session.get_projects()[2]

    def is_active(self):
        url = 'https://api.clockify.me/api/v1/workspaces/{}/user/{}/time-entries'
        re = requests.get(url.format(self.workspace_id, self.user_id), headers=self.headers)
        if not re.json()[0]['timeInterval']['end']:  # Если время окончания задачи не None
            return True
        else:
            return False

    def start_task(self, description):
        moscow_time = datetime.now(self.zone)  # текущее время по Москве
        response = self.session.add_time_entry(
            start_time=moscow_time, description=description, project=self.project
            # В проектеWork начинается отсчёт времени
        )  # с названием discription

        print(response)

    def stop_task(self):
        moscow_time = datetime.now(self.zone)
        self.session.stop_timer(stop_time=moscow_time)

    def get_dt_start(self):  # ,task_name):
        tasks = requests.get(
            'https://api.clockify.me/api/v1/workspaces/{}/user/{}/time-entries'.format(self.workspace_id, self.user_id),
            headers=self.headers).json()
        # duration=[{task['name']:task[0]['timeInterval']['duration']} for task in tasks]
        time_start = tasks[0]['timeInterval']['start']
        time_start = datetime.strptime(time_start, "%Y-%m-%dT%H:%M:%SZ")
        return time_start
