import pandas as pd
pd.set_option('display.max_columns', None)

column_headers = ['sale', 'sales_amount_in_euro', 'time_delay_for_conversion',
                  'click_timestamp', 'nb_clicks_1week', 'product_price', 'product_age_group',
                  'device_type', 'audience_id', 'product_gender', 'product_brand',
                  'product_category1', 'product_category2', 'product_category3',
                  'product_category4', 'product_category5', 'product_category6',
                  'product_category7', 'product_country', 'product_id', 'product_title',
                  'partner_id', 'user_id']

clicks_df = pd.read_csv('../dataset/CriteoSearchData',
                        names=column_headers, delim_whitespace=True)

print(clicks_df[column_headers][:10])
