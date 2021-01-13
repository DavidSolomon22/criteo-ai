import random
import pandas as pd
from typing import List
import json
from datetime import datetime, timedelta


# optymalizuje ktore produkty wykluczyc z reklamy
class Optimizer:
    def __init__(self, partner_id: str, strategy: str, per_partner_average_click_cost: float):
        self.days = []
        self.productsSeenSoFar = []
        self.partner_id = partner_id
        self.previous_day = None
        self.strategy = strategy
        self.per_partner_average_click_cost = per_partner_average_click_cost
        self.profit_gain = []
        self.sustained_profit = []
        self.accumulated_profit_gain = []
        self.accumulated_sustained_profit = []
        self.accumulated_profit_gain_ratio = []

    def next_day(self, today_df: pd.DataFrame):
        today_products_df = set(today_df['product_id'])

        how_many_ratio = 3.1  # how_many_ratio for plotting
        # how_many_ratio = 20  # how_many_ratio for logs

        productsToExclude = self.__get_excluded_products_pseudorandomly(
            how_many_ratio, 12)
        productsToExcludeSet = set(productsToExclude)
        productsActuallyExcluded = sorted(list(productsToExcludeSet.intersection(
            today_products_df)))

        self.__add_missing_days(today_df['click_timestamp'].iloc[0])

        cliks_on_actually_excluded_products = today_df[today_df['product_id'].isin(
            productsActuallyExcluded)]

        cliks_on_not_actually_excluded_products = today_df[~today_df['product_id'].isin(
            productsActuallyExcluded)]

        today_profit_gain = self.calculate_profit(
            cliks_on_actually_excluded_products)

        today_sustained_profit = self.calculate_profit(
            cliks_on_not_actually_excluded_products)

        today_sustained_profit = today_sustained_profit * -1

        self.profit_gain.append(today_profit_gain)
        self.sustained_profit.append(today_sustained_profit)

        today_accumulated_profit_gain = 0
        today_accumulated_sustained_profit = 0

        if(len(self.accumulated_profit_gain) == 0):
            today_accumulated_profit_gain = today_profit_gain
            today_accumulated_sustained_profit = today_sustained_profit
            self.accumulated_profit_gain.append(today_accumulated_profit_gain)
            self.accumulated_sustained_profit.append(
                today_accumulated_sustained_profit)
        else:
            today_accumulated_profit_gain = self.accumulated_profit_gain[-1] + \
                today_profit_gain
            today_accumulated_sustained_profit = self.accumulated_sustained_profit[-1] + \
                today_sustained_profit
            self.accumulated_profit_gain.append(today_accumulated_profit_gain)
            self.accumulated_sustained_profit.append(
                today_accumulated_sustained_profit)

        today_profit_ratio = (today_accumulated_profit_gain /
                              today_accumulated_sustained_profit)

        if(today_accumulated_sustained_profit != 0):
            self.accumulated_profit_gain_ratio.append(today_profit_ratio)

        day = {
            "day": today_df['click_timestamp'].iloc[0],
            # produkty z ostatnich dni
            "productsSeenSoFar": self.productsSeenSoFar,
            # produkty ktore zostaly wykluczone z reklamy
            "productsToExclude": productsToExclude,
            # produkty ktore zostaly faktycznie wykluczone z reklamy
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
        print(
            '\n---------------------------------------------------------------------------------------------------------------------------------')
        print('\nExcluded products log generated at path: ', f'"{filename}"')

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

                self.profit_gain.append(0)
                self.sustained_profit.append(0)
                self.accumulated_profit_gain.append(
                    self.accumulated_profit_gain[-1])
                self.accumulated_sustained_profit.append(
                    self.accumulated_sustained_profit[-1])
                self.accumulated_profit_gain_ratio.append(
                    self.accumulated_profit_gain_ratio[-1])

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
        print('\nexcluded-products-log: ', first_log_path)
        print('verification-log: ', second_log_path)
        with open(first_log_path) as first_log_file:
            first_log_json = json.load(first_log_file)
        with open(second_log_path) as second_log_file:
            second_log_json = json.load(second_log_file)
        return first_log_json == second_log_json

    def calculate_profit(self, clicks_df: pd.DataFrame):
        number_of_clicks_per_day = len(clicks_df)
        partner_income = clicks_df[clicks_df['SalesAmountInEuro']
                                   >= 0]['SalesAmountInEuro'].sum()
        return (number_of_clicks_per_day * self.per_partner_average_click_cost) - (partner_income * 0.22)
