from partner_data_reader import PartnerDataReader
from optimizer import Optimizer

if __name__ == "__main__":
    partner_id = 'C0F515F0A2D0A5D9F854008BA76EB537'
    partner_data = PartnerDataReader(partner_id)
    partner_clicks_df = partner_data.parnter_clicks_df
    del partner_clicks_df[3:8]
    optimizer = Optimizer(partner_clicks_df, partner_id)

    for i in range(len(optimizer.partner_data) - 1):
        today_df = optimizer.partner_data[i]
        optimizer.next_day(today_df, i)
    optimizer.log_optimizations()

    # print(partner_data_reader.parnter_clicks_df)
    # print(partner_data_reader.per_partner_average_click_cost)
    # print(partner_data_reader.total_number_of_clicks)
    # print(partner_data_reader.total_sales_amount_in_euro)
