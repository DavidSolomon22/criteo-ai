from partner_data_reader import PartnerDataReader
from optimizer import Optimizer

if __name__ == "__main__":
    partner_id = '04A66CE7327C6E21493DA6F3B9AACC75'
    strategy = 'random'
    partner_data = PartnerDataReader(partner_id)
    # partner_clicks_df = partner_data.parnter_clicks_df
    # del partner_clicks_df[3:8]
    # optimizer = Optimizer(partner_clicks_df, partner_id, strategy)
    optimizer = Optimizer(partner_data.parnter_clicks_df, partner_id, strategy)

    for i in range(len(optimizer.partner_data) - 1):
        today_df = optimizer.partner_data[i]
        optimizer.next_day(today_df, i)

    optimizer.log_optimizations()

    first_log_path = f'../data/excluded-products-logs/{strategy}/partner_{partner_id}.json'
    second_log_path = f'../data/verification-logs/{strategy}/mr-riegel/partner_{partner_id}.json'
    are_logs_equal = optimizer.compare_logs(first_log_path, second_log_path)
    print(are_logs_equal)
