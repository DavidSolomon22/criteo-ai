import pandas as pd
from typing import List


class PartnerDataReader:

    def __init__(self, partner_id: str):
        self.parnter_clicks_df = self.__read_partner_clicks(partner_id)

        self.total_number_of_clicks = self.__calc_total_number_of_clicks(
            self.parnter_clicks_df)

        self.total_sales_amount_in_euro = self.__calc_total_sales_amount_in_euro(
            self.parnter_clicks_df)

        self.per_partner_average_click_cost = self.__calc_per_partner_average_click_cost(
            self.total_sales_amount_in_euro, self.total_number_of_clicks)

        self.__convert_timestamp(self.parnter_clicks_df)
        self.parnter_clicks_df = self.__group_df_by_day(self.parnter_clicks_df)

    def next_day(self):
        pass

    def __read_partner_clicks(self, partner_id: str) -> pd.DataFrame:
        filename = f'../data/criteo-dataset-splitted/partner_{partner_id}.csv'
        return pd.read_csv(filename, index_col=0)

    def __convert_timestamp(self, parnter_clicks_df: pd.DataFrame) -> None:
        parnter_clicks_df['click_timestamp'] = parnter_clicks_df['click_timestamp'].apply(
            lambda x: str(pd.to_datetime(int(x), unit='s').date()))

    def __group_df_by_day(self, parnter_clicks_df: pd.DataFrame) -> List[pd.DataFrame]:
        return [group for index, group in parnter_clicks_df.groupby('click_timestamp')]

    def __calc_total_number_of_clicks(self, parnter_clicks_df: pd.DataFrame) -> int:
        return len(parnter_clicks_df)

    def __calc_total_sales_amount_in_euro(self, parnter_clicks_df: pd.DataFrame) -> float:
        return parnter_clicks_df.loc[parnter_clicks_df['SalesAmountInEuro']
                                     != -1.0].SalesAmountInEuro.sum()

    def __calc_per_partner_average_click_cost(self, total_sales_amount_in_euro: float, total_number_of_clicks: int) -> float:
        return 0.12 * total_sales_amount_in_euro / total_number_of_clicks
