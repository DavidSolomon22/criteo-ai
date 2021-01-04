from partner_data_reader import PartnerDataReader
from optimizer import Optimizer


class Simulator:
    def __init__(self, partner_id: str, exclusion_strategy: str):
        self.partner_id = partner_id
        self.exclusion_strategy = exclusion_strategy

    def run_simulation(self):
        partner_data = PartnerDataReader(self.partner_id)
        optimizer = Optimizer(self.partner_id, self.exclusion_strategy)

        for i in range(len(partner_data.parnter_clicks_per_day_dfs) - 1):
            today_df = partner_data.parnter_clicks_per_day_dfs[i]
            optimizer.next_day(today_df)

        optimizer.log_optimizations()

        first_log_path = f'../data/excluded-products-logs/{self.exclusion_strategy}/partner_{self.partner_id}.json'
        second_log_path = f'../data/verification-logs/{self.exclusion_strategy}/mr-riegel/partner_{self.partner_id}.json'
        are_logs_equal = optimizer.compare_logs(
            first_log_path, second_log_path)

        if are_logs_equal:
            print('\nGenerated log is the same as verification log.')
        else:
            print('\nGenerated log is not the same as verification log.')
        print(
            '\n---------------------------------------------------------------------------------------------------------------------------------')

        print(f'\nParameters calculated per partner {self.partner_id}:\n')
        print('total_number_of_clicks:', partner_data.total_number_of_clicks)
        print('total_sales_amount_in_euro:',
              partner_data.total_sales_amount_in_euro)
        print('per_partner_average_click_cost:',
              partner_data.per_partner_average_click_cost)
        print(
            '\n---------------------------------------------------------------------------------------------------------------------------------\n')
