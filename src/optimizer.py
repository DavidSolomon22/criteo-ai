import random
import pandas as pd
from typing import List
import json
from datetime import datetime, timedelta


# optymalizuje ktore produkty wykluczyc z reklamy na dzisiejszy/jutrzejszy dzien (zalezy od interepretacji)
class Optimizer:
    def __init__(self, partner_data: List[pd.DataFrame], partner_id: str, strategy: str):
        self.partner_data = partner_data
        self.days = []
        self.productsSeenSoFar = []
        self.partner_id = partner_id
        self.previous_day = None
        self.strategy = strategy

    def next_day(self, today_df: pd.DataFrame, index: int):
        today_products_df = set(today_df['product_id'])
        productsToExclude = self.__get_excluded_products_pseudorandomly(
            20, 12)
        productsToExcludeSet = set(productsToExclude)
        productsActuallyExcluded = sorted(list(productsToExcludeSet.intersection(
            today_products_df)))

        self.__add_missing_days(today_df['click_timestamp'].iloc[0])

        day = {
            "day": today_df['click_timestamp'].iloc[0],
            # produkty z ostatnich dni
            "productsSeenSoFar": self.productsSeenSoFar,
            # produkty ktore zostaly wykluczone z reklamy na dzien dzisiejszy, na podstawie jakiegos algorytmu (algorytm dziala tylko na danych historycznych - productsSeenSoFar)
            "productsToExclude": productsToExclude,
            # produkty ktore zostaly faktycznie wykluczone z dnia dzisiejszego
            "productsActuallyExcluded": productsActuallyExcluded
        }
        self.days.append(day)

        productsSeenSoFarSet = set(self.productsSeenSoFar)
        productsSeenSoFarSet.update(today_products_df)
        self.productsSeenSoFar = sorted(list(productsSeenSoFarSet))
        self.previous_day = today_df['click_timestamp'].iloc[0]

    def log_optimizations(self):
        filename = f'../data/excluded-products-logs/{self.strategy}/partner_{self.partner_id}.json'
        log = {
            "strategy": self.strategy,
            "days": self.days
        }
        with open(filename, 'w') as f:
            json.dump(log, f, indent=2)

    def __get_excluded_products_pseudorandomly(self, how_many_ratio: float, random_seed: int):
        dummy_list_of_potentially_excluded_products = self.productsSeenSoFar

        dummy_list_of_potentially_excluded_products.sort()
        dummy_how_many_products = round(
            len(dummy_list_of_potentially_excluded_products) / how_many_ratio)
        random.seed(random_seed)

        excluded_products = random.sample(
            dummy_list_of_potentially_excluded_products, dummy_how_many_products)
        return sorted(excluded_products)

    def __add_missing_days(self, today_date):
        if(self.previous_day == None):
            return

        today_date_as_date = datetime.strptime(today_date, '%Y-%m-%d')
        previous_date_as_date = datetime.strptime(
            self.previous_day, '%Y-%m-%d')

        dates_subtraction = today_date_as_date - previous_date_as_date

        if dates_subtraction.days > 1:
            for i in range(dates_subtraction.days - 1):
                index = ((dates_subtraction.days - 1) - i)
                day_to_add = today_date_as_date - \
                    timedelta(days=index)

                self.days.append(
                    self.__generate_empty_day(day_to_add))

    def __generate_empty_day(self, date):
        return {
            "day": datetime.strftime(date, '%Y-%m-%d'),
            "productsSeenSoFar": [],
            "productsToExclude": [],
            "productsActuallyExcluded": []
        }

    def compare_logs(self, first_log_path: str, second_log_path: str) -> bool:
        with open(first_log_path) as first_log_file:
            first_log_json = json.load(first_log_file)
        with open(second_log_path) as second_log_file:
            second_log_json = json.load(second_log_file)

        print(first_log_path)
        print(second_log_path)
        return first_log_json == second_log_json
