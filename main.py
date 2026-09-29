import logging
import json
import uuid
import random
import time

from queries import Query
from scenarios import (query_and_preserve, query_and_pay, query_and_consign, query_and_cancel,
                       query_and_collect, query_and_execute, query_and_rebook, query_and_get_voucher)
from datetime import datetime, timedelta, date
from locust import HttpUser, task, between, constant, events


def chance(p: float) -> bool:
    return random.random() < p


def pause():
    time.sleep(random.randint(1, 5))


class UserBooking(HttpUser):
    wait_time = between(2, 10)

    @task
    def query_and_preserve(self):
        print("Perform user tasks")
        # login
        query = Query(ts_address=self.host)
        query.login()

        query.query_normal_ticket()
        pause()

        # 1 out of 3 clients will perform query and preserve, and query and pay
        if chance(1 / 3):
            query_and_preserve(query)
            pause()

        if chance(1 / 3):
            query_and_pay(query)
            pause()

        if chance(1 / 10):
            query_and_consign(query)
            pause()

        if chance(1 / 4):
            query.query_high_speed_ticket()
            pause()

        if chance(1 / 4):
            query.query_food()
            pause()

        if chance(1 / 4):
            query.query_advanced_ticket(type=random.choice(["cheapest", "quickest", "minStation"]))
            pause()

        # after-sale flows: cancel, collect, enter station, rebook, voucher
        if chance(1 / 10):
            query_and_cancel(query)
            pause()

        if chance(1 / 10):
            query_and_collect(query)
            pause()

        if chance(1 / 10):
            query_and_execute(query)
            pause()

        if chance(1 / 10):
            query_and_rebook(query)
            pause()

        if chance(1 / 10):
            query_and_get_voucher(query)
            pause()

        if chance(1 / 5):
            query.query_news()
            query.query_offices()

    @task
    def admin_tasks(self):
        print("Perform admin tasks")
        # login
        query = Query(ts_address=self.host)
        query.login(username="admin", password="222222")
        query.query_admin_travel()
        pause()
        query.query_admin_basic_price()
        pause()
        query.query_admin_basic_config()
        pause()
        query.query_admin_order()
        query.query_admin_route()
        query.query_admin_user()
