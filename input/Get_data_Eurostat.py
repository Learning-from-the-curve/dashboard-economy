import os
import eurostat

# Define function to get data from Eurostat
def data_Eurostat(url, container):
    ind = 0
    while ind < len(url):
        container.append([url[ind][0], eurostat.get_data_df(url[ind][1])])
        ind += 1

# Save all data
def store_data(path):
    os.makedirs(path, exist_ok = True)
    ind = 0
    while ind < len(EU):
        EU[ind][1].to_csv(path + EU[ind][0] + '.csv', index = False)
        ind += 1

# Define Eurostat codes to call
Eurostat_code = [['Consumer_monthly_data', 'ei_bsco_m'],
                 ['Industry_monthly_data', 'ei_bsin_m_r2'],
                 ['Construction_monthly_data', 'ei_bsbu_m_r2'],
                 ['Retail_sale_monthly_data', 'ei_bsrt_m_r2'],
                 ['Sentiment_indicator_monthly_data', 'ei_bssi_m_r2'],
                 ['Services_monthly_data', 'ei_bsse_m_r2'],
                 ['EU_Business_climate_indicator_monthly_data', 'ei_bsci_m_r2'],
                 ['Harmonized_index_of_consumer_prices_monthly_data', 'ei_cphi_m'],
                 ['Energy_monthly_data', 'ei_isen_m'],
                 ['Unemployment_by_sex_and_age_monthly_data', 'une_rt_m'],
                 ['Job_vacancy_rate', 'ei_lmjv_q_r2'],
                 ['Interest_rate_monthly_data', 'ei_mfir_m'],
                 ['GDP_and_main_components', 'nama_10_gdp'],
                 ['Gross_value_added_and_income_by_industry', 'namq_10_a10'],
                 ['Employmentby_industry', 'namq_10_a10_e'],
]            

# Download all data
EU  = []
data_Eurostat(Eurostat_code, EU)

store_data(os.getcwd() + "/Eurostat_data/")
