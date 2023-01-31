# import pytest
# from datetime import datetime
# import time


def test_connections(connect):
    notion, clockify = connect
    assert notion is not None
    assert clockify is not None


def test_clockify(connect):
    _, clockify = connect
    assert clockify.is_active() is False
    # start_time = datetime.now()
    clockify.start_task("test_task")
    assert clockify.is_active() is True
    clockify.stop_task()
    assert clockify.is_active() is False


def test_notion_without_checkbox(connect):
    notion, _ = connect
    assert type(notion.pages) is list
    assert type(notion.pages[0]) is dict
    # print(notion.work_pages)
    # print(notion.work_pages_id)
    assert notion.work_pages == []
    assert notion.work_pages_id == []
    assert notion.get_time() == {}
    # print(notion.get_time())
