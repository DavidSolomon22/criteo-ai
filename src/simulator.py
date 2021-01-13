from partner_data_reader import PartnerDataReader
from optimizer import Optimizer
from matplotlib import pyplot as plt


class Simulator:
    def __init__(self, partner_id: str, exclusion_strategy: str):
        self.partner_id = partner_id
        self.exclusion_strategy = exclusion_strategy

    def run_simulation(self):
        partner_data = PartnerDataReader(self.partner_id)
        optimizer = Optimizer(self.partner_id, self.exclusion_strategy,
                              partner_data.per_partner_average_click_cost)

        for i in range(len(partner_data.parnter_clicks_per_day_dfs) - 1):
            today_df = partner_data.parnter_clicks_per_day_dfs[i]
            optimizer.next_day(today_df)

        self.__plot(optimizer)

        optimizer.log_optimizations()

        first_log_path = f'../data/excluded-products-logs/{self.exclusion_strategy}/partner_{self.partner_id}.json'
        second_log_path = f'../data/verification-logs/{self.exclusion_strategy}/mr-riegel/partner_{self.partner_id}.json'
        are_logs_equal = optimizer.compare_logs(
            first_log_path, second_log_path)

        self.__console_log(are_logs_equal, partner_data)

    def __plot(self, optimizer):
        self.__plot_first_comparision(optimizer)
        self.__plot_second_comparision(optimizer)
        self.__plot_third_comparision(optimizer)
        self.__plot_sustained_profit(optimizer)
        self.__plot_accumulated_sustained_profit(optimizer)
        self.__plot_profit_gain(optimizer)
        self.__plot_accumulated_profit_gain(optimizer)
        self.__plot_accumulated_profit_gain_ratio(optimizer)

    def __plot_first_comparision(self, optimizer: Optimizer):
        plt.figure(figsize=(9, 1))
        plt.plot(optimizer.profit_gain_list, label="Profit gain")
        plt.plot(optimizer.sustained_profit_list, label="Sustained profit")
        plt.legend(loc="upper right")
        plt.ylabel('EUR')
        plt.xlabel('Days of simulation')
        plt.grid()
        plt.show()

    def __plot_second_comparision(self, optimizer: Optimizer):
        plt.figure(figsize=(9, 1))
        plt.plot(optimizer.accumulated_profit_gain,
                 label="Accumulated profit gain")
        plt.plot(optimizer.accumulated_sustained_profit,
                 label="Accumulated sustained profit")
        plt.legend(loc="upper right")
        plt.ylabel('EUR')
        plt.xlabel('Days of simulation')
        plt.grid()
        plt.show()

    def __plot_third_comparision(self, optimizer: Optimizer):
        plt.figure(figsize=(9, 1))
        plt.plot(optimizer.profit_ratio_list,
                 label="Accumulated profit gain ratio")
        plt.legend(loc="lower right")
        plt.ylabel('EUR')
        plt.xlabel('Days of simulation')
        plt.grid()
        plt.show()

    def __plot_sustained_profit(self, optimizer: Optimizer):
        plt.plot(optimizer.sustained_profit_list, label=self.partner_id)
        plt.legend(loc="lower right")
        plt.ylabel('Sustained profit')
        plt.xlabel('Days of simulation')
        plt.grid()
        plt.show()

    def __plot_accumulated_sustained_profit(self, optimizer: Optimizer):
        plt.plot(optimizer.accumulated_sustained_profit, label=self.partner_id)
        plt.legend(loc="upper left")
        plt.ylabel('Accumulated sustained profit')
        plt.xlabel('Days of simulation')
        plt.grid()
        plt.show()

    def __plot_profit_gain(self, optimizer: Optimizer):
        plt.plot(optimizer.profit_gain_list, label=self.partner_id)
        plt.legend(loc="lower right")
        plt.ylabel('Profit gain')
        plt.xlabel('Days of simulation')
        plt.grid()
        plt.show()

    def __plot_accumulated_profit_gain(self, optimizer: Optimizer):
        plt.plot(optimizer.accumulated_profit_gain, label=self.partner_id)
        plt.legend(loc="upper right")
        plt.ylabel('Accumulated profit gain')
        plt.xlabel('Days of simulation')
        plt.grid()
        plt.show()

    def __plot_accumulated_profit_gain_ratio(self, optimizer: Optimizer):
        plt.plot(optimizer.profit_ratio_list, label=self.partner_id)
        plt.legend(loc="upper right")
        plt.ylabel('Accumulated profit gain ratio')
        plt.xlabel('Days of simulation')
        plt.grid()
        plt.show()

    def __console_log(self, are_logs_equal, partner_data):
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
