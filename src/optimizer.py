import random
import pandas as pd
from typing import List
import json


# optymalizuje ktore produkty wykluczyc z reklamy na dzisiejszy/jutrzejszy dzien (zalezy od interepretacji)
class Optimizer:
    def __init__(self, partner_data: List[pd.DataFrame], partner_id: str):
        self.partner_data = partner_data
        self.days = []
        self.productsSeenSoFar = []
        self.partner_id = partner_id

    # DONE: - zamienic today_df na set w ktorym sa product_id
    # DONE: - przy kazdej iteracji (na sam koniec) dodawac set product_id (z today_df) do productsSeenSoFar
    # DONE: - obliczac productsToExclude
    def next_day(self, today_df: pd.DataFrame, index: int):
        today_products_df = set(today_df['product_id'])
        productsToExclude = self.__get_excluded_products_pseudorandomly(
            20, 12)
        productsToExcludeSet = set(productsToExclude)
        productsActuallyExcluded = sorted(list(productsToExcludeSet.intersection(
            today_products_df)))

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

    def log_optimizations(self):
        filename = f'partner_{self.partner_id}'
        log = {
            "strategy": "random",
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
