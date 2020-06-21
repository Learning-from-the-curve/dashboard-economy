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
                 #['Consumer_quarterly_data', 'ei_bsco_q'],
                 ['Industry_monthly_data', 'ei_bsin_m_r2'],
                 #['Industry_quarterly_data', 'ei_bsin_q_r2'],
                 ['Construction_monthly_data', 'ei_bsbu_m_r2'],
                 #['Construction_quarterly_data', 'ei_bsbu_q_r2'],
                 ['Retail_sale_monthly_data', 'ei_bsrt_m_r2'],
                 ['Sentiment_indicator_monthly_data', 'ei_bssi_m_r2'],
                 ['Services_monthly_data', 'ei_bsse_m_r2'],
                 #['Services_quarterly_data', 'ei_bsse_q_r2'],
                 ['EU_Business_climate_indicator_monthly_data', 'ei_bsci_m_r2'],
                 #['Financial_services_monthly_data', 'ei_bsfs_m'],
                 #['Financial_services_quarterly_data', 'ei_bsfs_q'],
                 #['Employment_expectation_indicator', 'ei_bsee_m_r2'],
                 #['Current_account_quarterly_data', 'ei_bpm6ca_q'],
                 #['Financial_account_quarterly_data', 'ei_bpm6fa_q'],
                 #['Current_account_monthly_data', 'ei_bpm6ca_m'],
                 #['Financial_account_monthly_data', 'ei_bpm6fa_m'],
                 #['International_investment_position_quarterly_data', 'ei_bpm6iip_q'],
                 ['Harmonized_index_of_consumer_prices_monthly_data', 'ei_cphi_m'],
                 #['International_trade_monthly_data_EU27', 'ei_eteu27_2020_m'],
                 #['International_trade_monthly_data_EU28', 'ei_eteu28_m'],
                 #['Euro_area_monthly_data_EU19', 'ei_etea19_m'],
                 #['Industry_monthly_data_index', 'ei_isin_m'],
                 #['Industry_monthly_growth_rates', 'ei_isir_m'],
                 #['Industry_quarterly_data_index', 'ei_isind_q'],
                 #['Construction_monthly_data_index', 'ei_isbu_m'],
                 #['Construction_monthly_growth_rates', 'ei_isbr_m'],
                 #['Construction_quarterly_data_index', 'ei_isbu_q'],
                 #['Retail_trade_monthly_data_growth_rates', 'ei_isrr_m'],
                 #['Retail_trade_quarterly_data_growth_rates', 'ei_isrt_q'],
                 #['Turnover_in_services_quarterly_data_index', 'ei_isset_q'],
                 #['Turnover_in_services_quarterly_data_growth_rates', 'ei_isse_q'],
                 #['Service_producer_prices_quarterly_data_index', 'ei_isppi_q'],
                 #['Service_producer_prices_quarterly_data_growth_rates', 'ei_isppe_q'],
                 ['Energy_monthly_data', 'ei_isen_m'],
                 ['Unemployment_by_sex_and_age_monthly_data', 'une_rt_m'],
                 #['Harmonized_unemployment_rates_monthly_data', 'ei_lmhr_m'],
                 #['Labour_cost_index_nominal_value_quarterly_data', 'ei_lmlc_q'],
                 ['Job_vacancy_rate', 'ei_lmjv_q_r2'],
                 ['Interest_rate_monthly_data', 'ei_mfir_m'],
                 #['ECU_Euro_exchange_rate_monthly_data', 'ei_mfrt_m'],
                 #['Effective_exchange_rate_indices_monthly_data', 'ei_mfef_m'],
                 ['GDP_and_main_components', 'nama_10_gdp'],
                 #['Main_GDP_aggregates', 'namq_10_gdp'],
                 #['Final_consumption_aggregates', 'namq_10_fcs'],
                 #['Exports_and_imports_by_member_states_of_the_EU_third_countries', 'namq_10_exi'],
                 ['Gross_value_added_and_income_by_industry', 'namq_10_a10'],
                 #['Gross_fixed_capital_formation_by_industry', 'namq_10_an6'],
                 ['Employmentby_industry', 'namq_10_a10_e'],
                 #['Key_indicators_sectors', 'nasq_10_ki'],
                 #['Non_financial_transactions', 'nasq_10_nf_tr'],
                 #['House_price_index_quarterly_data', 'ei_hppi_q'],
                 #['Area_by_NUTS3', 'reg_area3']
]            

# Download all data
EU  = []
data_Eurostat(Eurostat_code, EU)

store_data(os.getcwd() + "/Eurostat_data/")
