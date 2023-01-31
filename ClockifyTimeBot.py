from datetime import datetime
import time
import os
from NotionParser import Parser, add_time
from ClockifyUpdater import ClockifyUpdater
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
CLOCKIFY_TOKEN = os.getenv("CLOCKIFY_TOKEN")
CLOCKIFY_WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
CLOCKIFY_USER_ID = os.getenv("CLOCKIFY_USER_ID")


def get_sec(time_str):
    """Get Seconds from time."""
    try:
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)
    except ValueError:
        return time_str


def get_rubls(notion):
    return {'today': sum((datetime.strptime(page['Time done']['last_edited_time'],
                                            '%Y-%m-%dT%H:%M:%S.000Z').date() == datetime.now().date() and
                          page['Done']['checkbox'] for page in notion.pages)) * 273.73,
            'all_time': sum((page['Done']['checkbox'] for page in notion.pages)) * 273.73}


def main():
    flag = 0
    notion = Parser(NOTION_TOKEN)
    clockify = ClockifyUpdater(CLOCKIFY_TOKEN, CLOCKIFY_WORKSPACE_ID, CLOCKIFY_USER_ID)
    # active_pages, active_pages_id = notion.get_work_pages_id()
    rubls = get_rubls(notion)
    while 1:
        active_pages, active_pages_id = notion.get_work_pages_id()
        past_rubls = rubls
        rubls = get_rubls(notion)
        print(active_pages_id)
        if past_rubls['today'] != rubls['today']:
            notion.update_page_today(rubls['today'])
        if past_rubls['all_time'] != rubls['all_time']:
            notion.update_page_total(rubls['all_time'])
        if active_pages:
            if flag == 1:
                page_name = active_pages[0]['Name']['title'][0]['plain_text']
                clockify.start_task(page_name)
                start = datetime.now()
                time_past = get_sec(notion.get_time()[active_pages_id[0]])
                print('Отсчёт времени для задачи: ' + page_name)
                flag = 0
            tmdlt = datetime.now() - start

            format_time = add_time(tmdlt.seconds, time_past, page_id=active_pages_id[0], token=NOTION_TOKEN)
            print(f"{format_time}\r", end="")
            time.sleep(1)
        else:
            is_actv = clockify.is_active()
            if is_actv:
                clockify.stop_task()
                print('\n' + page_name + ' остановлен')
            flag = 1
            time.sleep(1)


if __name__ == '__main__':
    main()
