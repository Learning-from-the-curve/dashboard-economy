import pickle
import json
import pandas as pd
import numpy as np
from pathlib import Path
from process_functions import list_diff, list_union, write_log, eurostat_columns_df
from pickle_functions import picklify, unpicklify

######################################
# Retrieve data
######################################

# Paths
path_grossVA = Path.cwd() / 'Eurostat_data' / 'Gross_value_added_and_income_by_industry.csv'
path_employment = Path.cwd() / 'Eurostat_data' / 'Employmentby_industry.csv'
path_GDP = Path.cwd() / 'Eurostat_data' / 'GDP_and_main_components.csv'
path_HICP = Path.cwd() / 'Eurostat_data' / 'Harmonized_index_of_consumer_prices_monthly_data.csv'
path_HU = Path.cwd() / 'Eurostat_data' / 'Unemployment_by_sex_and_age_monthly_data.csv'
path_BC = Path.cwd() / 'Eurostat_data' / 'EU_Business_climate_indicator_monthly_data.csv'
path_construction = Path.cwd() / 'Eurostat_data' / 'Construction_monthly_data.csv'
path_consumer = Path.cwd() / 'Eurostat_data' / 'Consumer_monthly_data.csv'
path_energy = Path.cwd() / 'Eurostat_data' / 'Energy_monthly_data.csv'
path_industry = Path.cwd() / 'Eurostat_data' / 'Industry_monthly_data.csv'
path_interest = Path.cwd() / 'Eurostat_data' / 'Interest_rate_monthly_data.csv'
path_job = Path.cwd() / 'Eurostat_data' / 'Job_vacancy_rate.csv'
path_retail = Path.cwd() / 'Eurostat_data' / 'Retail_sale_monthly_data.csv'
path_sentiment = Path.cwd() / 'Eurostat_data' / 'Sentiment_indicator_monthly_data.csv'
path_services = Path.cwd() / 'Eurostat_data' / 'Services_monthly_data.csv'
path_ISO = Path.cwd() / 'input' / 'ISO.csv'

#########################################################################################
# import codes for countries
ISO = pd.read_csv(path_ISO)
#pd.set_option('display.max_rows', df.shape[0]+1)
start_date = 1900
end_date = 2022

#########################################################################################
# Data preprocessing for getting useful data and shaping data compatible to plotly plot
#########################################################################################

#first card: GDP
GDP = pd.read_csv(path_GDP)
GDP_card = eurostat_columns_df(GDP, 2019, end_date, dict_col = { "na_item": ["B1GQ"], "unit": ["CLV_I05"], r"geo\time": ["EU28"]})
GDP_card.reset_index(drop = True, inplace = True)
GDP_card = GDP_card.loc[:, ~(GDP_card.isnull()).any()]
#second card: HICP
HICP = pd.read_csv(path_HICP)
HICP_card = eurostat_columns_df(HICP, 2019, end_date, dict_col = {"indic": ["CP-HI00"], "s_adj": ["NSA"], "unit": ["HICP2015"], r"geo\time": ["EU28"]})
HICP_card.reset_index(drop = True, inplace = True)
HICP_card = HICP_card.loc[:, ~(HICP_card.isnull()).any()]
#third card: unemployment
HU = pd.read_csv(path_HU)
HU_card = eurostat_columns_df(HU, 2019, end_date, dict_col = {'sex': ['T'], "s_adj": ["SA"], 'age' : ['TOTAL'], "unit": ["PC_ACT"], r"geo\time": ["EU28"]})
HU_card.reset_index(drop = True, inplace = True)
HU_card = HU_card.loc[:, ~(HU_card.isnull()).any()]
#fourth card: businnes climate
BC = pd.read_csv(path_BC)
BC_card = eurostat_columns_df(BC, 2019, end_date, dict_col = {"indic": [], "s_adj": [], r"geo\time": []})
BC_card.reset_index(drop = True, inplace = True)
BC_card = BC_card.loc[:, ~(BC_card.isnull()).any()]

countries_aggr=[]

#first plot: GDP

GDP_plot = eurostat_columns_df(GDP, start_date, end_date, dict_col = { "na_item": ["B1GQ"], "unit": ["CLV_I05"], r"geo\time": []})
GDP_plot = GDP_plot.drop(['na_item','unit'], axis=1).reset_index(drop = True)

for geo in GDP_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        GDP_plot.at[GDP_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(GDP_plot[r"geo\time"])-set(['EA12','EU15'])))

GDP_plot = GDP_plot.set_index(r"geo\time").T
GDP_plot.drop(['EA12','EU15'], axis=1, inplace=True)

#second plot: HICP 
#   CP-HI00	HICP - All items (HICP=Harmonized Index of Consumer Prices)

HI00_plot = eurostat_columns_df(HICP, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['CP-HI00'], "unit": ["HICP2015"], r"geo\time": []})
HI00_plot = HI00_plot.drop(['indic','unit', 's_adj'], axis=1).reset_index(drop = True)

for geo in HI00_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        HI00_plot.at[HI00_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]


countries_aggr.append(list(set(HI00_plot[r"geo\time"])-set(['United States of America','EU','EA18']))) 

HI00_plot = HI00_plot.set_index(r"geo\time").T
HI00_plot.drop(['United States of America','EU','EA18'], axis=1, inplace=True)

#third plot: unemployment

HU_plot = eurostat_columns_df(HU, start_date, end_date, dict_col = {'sex': ['T'], "s_adj": ["SA"], 'age' : ['TOTAL'], "unit": ["PC_ACT"], r"geo\time": []})
HU_plot = HU_plot.drop(['sex', "s_adj", 'age', "unit"], axis=1).reset_index(drop = True)

for geo in HU_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        HU_plot.at[HU_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(HU_plot[r"geo\time"])-set(['United States of America','Japan','EU25','EA18','EU27_2007'])))

HU_plot = HU_plot.set_index(r"geo\time").T
HU_plot.drop(['United States of America','Japan','EU25','EA18','EU27_2007'], axis=1, inplace=True)

#third plot: job vacancy

job = pd.read_csv(path_job)
job_plot = eurostat_columns_df(job, start_date, end_date, dict_col = {"nace_r2": ['A-S'], "s_adj": ['NSA'], "indic": ['JOBRATE'], "sizeclas": ["TOTAL"], r"geo\time": []})
job_plot = job_plot.drop(['s_adj','nace_r2','sizeclas','indic'], axis=1).reset_index(drop = True)

for geo in job_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        job_plot.at[job_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(job_plot[r"geo\time"]))

job_plot = job_plot.set_index(r"geo\time").T

#fourth plot: sentiment indicator
SI = pd.read_csv(path_sentiment)
#construction
SI_Construction_plot = eurostat_columns_df(SI, start_date, end_date, dict_col = { "s_adj": ['SA'], "indic": ['BS-CCI-BAL'], r"geo\time": []})
SI_Construction_plot = SI_Construction_plot.drop(['s_adj','indic'], axis=1).reset_index(drop = True)

for geo in SI_Construction_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        SI_Construction_plot.at[SI_Construction_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(SI_Construction_plot[r"geo\time"]))

SI_Construction_plot = SI_Construction_plot.set_index(r"geo\time").T

#economic
SI_Economic_plot = eurostat_columns_df(SI, start_date, end_date, dict_col = { "s_adj": ['SA'], "indic": ['BS-ESI-I'], r"geo\time": []})
SI_Economic_plot = SI_Economic_plot.drop(['s_adj','indic'], axis=1).reset_index(drop = True)

for geo in SI_Economic_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        SI_Economic_plot.at[SI_Economic_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(SI_Economic_plot[r"geo\time"]))

SI_Economic_plot = SI_Economic_plot.set_index(r"geo\time").T

#industrial
SI_Industrial_plot = eurostat_columns_df(SI, start_date, end_date, dict_col = { "s_adj": ['SA'], "indic": ['BS-ICI-BAL'], r"geo\time": []})
SI_Industrial_plot = SI_Industrial_plot.drop(['s_adj','indic'], axis=1).reset_index(drop = True)

for geo in SI_Industrial_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        SI_Industrial_plot.at[SI_Industrial_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]
countries_aggr.append(list(SI_Industrial_plot[r"geo\time"]))

SI_Industrial_plot = SI_Industrial_plot.set_index(r"geo\time").T

#retail
SI_Retail_plot = eurostat_columns_df(SI, start_date, end_date, dict_col = { "s_adj": ['SA'], "indic": ['BS-RCI-BAL'], r"geo\time": []})
SI_Retail_plot = SI_Retail_plot.drop(['s_adj','indic'], axis=1).reset_index(drop = True)

for geo in SI_Retail_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        SI_Retail_plot.at[SI_Retail_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]
countries_aggr.append(list(SI_Retail_plot[r"geo\time"]))

SI_Retail_plot = SI_Retail_plot.set_index(r"geo\time").T

#consumer
SI_Consumer_plot = eurostat_columns_df(SI, start_date, end_date, dict_col = { "s_adj": ['SA'], "indic": ['BS-CSMCI-BAL'], r"geo\time": []})
SI_Consumer_plot = SI_Consumer_plot.drop(['s_adj','indic'], axis=1).reset_index(drop = True)

for geo in SI_Consumer_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        SI_Consumer_plot.at[SI_Consumer_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]
countries_aggr.append(list(SI_Consumer_plot[r"geo\time"]))

SI_Consumer_plot = SI_Consumer_plot.set_index(r"geo\time").T

#services
SI_Services_plot = eurostat_columns_df(SI, start_date, end_date, dict_col = { "s_adj": ['SA'], "indic": ['BS-SCI-BAL'], r"geo\time": []})
SI_Services_plot = SI_Services_plot.drop(['s_adj','indic'], axis=1).reset_index(drop = True)

for geo in SI_Services_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        SI_Services_plot.at[SI_Services_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]
countries_aggr.append(list(SI_Services_plot[r"geo\time"]))

SI_Services_plot = SI_Services_plot.set_index(r"geo\time").T

#fifth plot: retail sale

RS = pd.read_csv(path_retail)
RS_plot = eurostat_columns_df(RS, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['BS-RAS'], "unit": ["BAL"], r"geo\time": []})
RS_plot = RS_plot.drop(['s_adj','indic', 'unit'], axis=1).reset_index(drop = True)

for geo in RS_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        RS_plot.at[RS_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(RS_plot[r"geo\time"]))

RS_plot = RS_plot.set_index(r"geo\time").T

#fifth plot: services

SV = pd.read_csv(path_services)
SV_plot = eurostat_columns_df(SV, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['BS-SCI'], "unit": ["BAL"], r"geo\time": []})
SV_plot = SV_plot.drop(['s_adj','indic', 'unit'], axis=1).reset_index(drop = True)

for geo in SV_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        SV_plot.at[SV_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(SV_plot[r"geo\time"]))

SV_plot = SV_plot.set_index(r"geo\time").T

#fifth plot: Consumer

CN = pd.read_csv(path_consumer)
CN_plot = eurostat_columns_df(CN, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['BS-CSMCI'], "unit": ["BAL"], r"geo\time": []})
CN_plot = CN_plot.drop(['s_adj','indic', 'unit'], axis=1).reset_index(drop = True)

for geo in CN_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        CN_plot.at[CN_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(CN_plot[r"geo\time"]))

CN_plot = CN_plot.set_index(r"geo\time").T

#sixth plot: Interest rate

IRST = pd.read_csv(path_interest)

#	Long term government bond yields - Maastricht definition
IRST_LTGBY_plot = eurostat_columns_df(IRST, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['MF-LTGBY-RT'], "p_adj": ["NAP"], r"geo\time": []})
IRST_LTGBY_plot = IRST_LTGBY_plot.drop(['s_adj','indic', 'p_adj'], axis=1).reset_index(drop = True)

for geo in IRST_LTGBY_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        IRST_LTGBY_plot.at[IRST_LTGBY_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(IRST_LTGBY_plot[r"geo\time"]))

IRST_LTGBY_plot = IRST_LTGBY_plot.set_index(r"geo\time").T

#seventh plot: Industry

IND = pd.read_csv(path_industry)
IND_plot = eurostat_columns_df(IND, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['BS-ICI'], "unit": ["BAL"], r"geo\time": []})
IND_plot = IND_plot.drop(['s_adj','indic', 'unit'], axis=1).reset_index(drop = True)

for geo in IND_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        IND_plot.at[IND_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(IND_plot[r"geo\time"]))

IND_plot = IND_plot.set_index(r"geo\time").T

#eighth plot: Construction

CSTR = pd.read_csv(path_construction)
CSTR_plot = eurostat_columns_df(CSTR, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['BS-CCI-BAL'], r"geo\time": []})
CSTR_plot = CSTR_plot.drop(['s_adj','indic',], axis=1).reset_index(drop = True)

for geo in CSTR_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        CSTR_plot.at[CSTR_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(CSTR_plot[r"geo\time"]))

CSTR_plot = CSTR_plot.set_index(r"geo\time").T

#eighth plot: Energy

# prod electr
EN = pd.read_csv(path_energy)
PEL_plot = eurostat_columns_df(EN, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['IS-PEL-GWH'], r"geo\time": []})
PEL_plot = PEL_plot.drop(['s_adj','indic',], axis=1).reset_index(drop = True)

for geo in PEL_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        PEL_plot.at[PEL_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(PEL_plot[r"geo\time"])-set(['EU27_2007'])))

PEL_plot = PEL_plot.set_index(r"geo\time").T
PEL_plot.drop(['EU27_2007'], axis=1, inplace=True)
#	Day-to-day money market
IRST_DDI_plot = eurostat_columns_df(IRST, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['MF-DDI-RT'], "p_adj": ["NAP"], r"geo\time": []})
IRST_DDI_plot = IRST_DDI_plot.drop(['s_adj','indic', 'p_adj'], axis=1).reset_index(drop = True)

for geo in IRST_DDI_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        IRST_DDI_plot.at[IRST_DDI_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(IRST_DDI_plot[r"geo\time"])-set(['United States of America','Japan'])))

IRST_DDI_plot = IRST_DDI_plot.set_index(r"geo\time").T
IRST_DDI_plot.drop(['United States of America','Japan'], axis=1, inplace=True)

#	3-month
IRST_3M_plot = eurostat_columns_df(IRST, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['MF-3MI-RT'], "p_adj": ["NAP"], r"geo\time": []})
IRST_3M_plot = IRST_3M_plot.drop(['s_adj','indic', 'p_adj'], axis=1).reset_index(drop = True)

for geo in IRST_3M_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        IRST_3M_plot.at[IRST_3M_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(IRST_3M_plot[r"geo\time"])-set(['United States of America','Japan'])))

IRST_3M_plot = IRST_3M_plot.set_index(r"geo\time").T
IRST_3M_plot.drop(['United States of America','Japan'], axis=1, inplace=True)

#first plot: gross va 
grossVA = pd.read_csv(path_grossVA)

grossVA_plot = eurostat_columns_df(grossVA, start_date, end_date, dict_col = { 'unit': ['CLV_I05'], "na_item": ['B1G'], "s_adj": ['NSA'], "nace_r2": ['TOTAL'], r"geo\time": []})
grossVA_plot = grossVA_plot.drop(['unit','s_adj','nace_r2','na_item'], axis=1).reset_index(drop = True)

for geo in grossVA_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        grossVA_plot.at[grossVA_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(grossVA_plot[r"geo\time"])-set([ 'EA12', 'EU15'])))

grossVA_plot = grossVA_plot.set_index(r"geo\time").T
grossVA_plot.drop([ 'EA12', 'EU15'], axis=1, inplace=True)

#second plot: employment 
employment = pd.read_csv(path_employment)

employment_plot = eurostat_columns_df(employment, start_date, end_date, dict_col = { "s_adj": ['SCA'], "nace_r2": ['TOTAL'], "unit": ['PCH_PRE_PER'], "na_item": ['EMP_DC'], r"geo\time": []})
employment_plot = employment_plot.drop(['unit','nace_r2','s_adj','na_item'], axis=1).reset_index(drop = True)

for geo in employment_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        employment_plot.at[employment_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(employment_plot[r"geo\time"])-set(['EA12', 'EU15'])))

employment_plot = employment_plot.set_index(r"geo\time").T
employment_plot.drop(['EA12', 'EU15'], axis=1, inplace=True)
# consumed electr
EN = pd.read_csv(path_energy)
CEL_plot = eurostat_columns_df(EN, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['IS-CEL-GWH'], r"geo\time": []})
CEL_plot = CEL_plot.drop(['s_adj','indic',], axis=1).reset_index(drop = True)

for geo in CEL_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        CEL_plot.at[CEL_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(CEL_plot[r"geo\time"])-set(['EU27_2007'])))

CEL_plot = CEL_plot.set_index(r"geo\time").T
CEL_plot.drop(['EU27_2007'], axis=1, inplace=True)
# import electr
EN = pd.read_csv(path_energy)
IEL_plot = eurostat_columns_df(EN, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['IS-IEL-GWH'], r"geo\time": []})
IEL_plot = IEL_plot.drop(['s_adj','indic',], axis=1).reset_index(drop = True)

for geo in IEL_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        IEL_plot.at[IEL_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(IEL_plot[r"geo\time"])-set(['EU27_2007'])))

IEL_plot = IEL_plot.set_index(r"geo\time").T
IEL_plot.drop(['EU27_2007'], axis=1, inplace=True)
# prod gas
EN = pd.read_csv(path_energy)
PNG_plot = eurostat_columns_df(EN, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['IS-PNG-TJ'], r"geo\time": []})
PNG_plot = PNG_plot.drop(['s_adj','indic',], axis=1).reset_index(drop = True)

for geo in PNG_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        PNG_plot.at[PNG_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(PNG_plot[r"geo\time"])-set(['EU27_2007'])))

PNG_plot = PNG_plot.set_index(r"geo\time").T
PNG_plot.drop(['EU27_2007'], axis=1, inplace=True)
# consumed gas
EN = pd.read_csv(path_energy)
CNG_plot = eurostat_columns_df(EN, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['IS-CNG-TJ'], r"geo\time": []})
CNG_plot = CNG_plot.drop(['s_adj','indic',], axis=1).reset_index(drop = True)

for geo in CNG_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        CNG_plot.at[CNG_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(CNG_plot[r"geo\time"])-set(['EU27_2007'])))

CNG_plot = CNG_plot.set_index(r"geo\time").T
CNG_plot.drop(['EU27_2007'], axis=1, inplace=True)
# import gas
EN = pd.read_csv(path_energy)
ING_plot = eurostat_columns_df(EN, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['IS-ING-TJ'], r"geo\time": []})
ING_plot = ING_plot.drop(['s_adj','indic',], axis=1).reset_index(drop = True)

for geo in ING_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        ING_plot.at[ING_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]

countries_aggr.append(list(set(ING_plot[r"geo\time"])-set(['EU27_2007'])))

ING_plot = ING_plot.set_index(r"geo\time").T
ING_plot.drop(['EU27_2007'], axis=1, inplace=True)

#	CP-HIIG	HICP - Industrial goods

HIIG_plot = eurostat_columns_df(HICP, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['CP-HIIG'], "unit": ["HICP2015"], r"geo\time": []})
HIIG_plot = HIIG_plot.drop(['indic','unit', 's_adj'], axis=1).reset_index(drop = True)

for geo in HIIG_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        HIIG_plot.at[HIIG_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]


countries_aggr.append(list(set(HIIG_plot[r"geo\time"])-set(['EU','EA18']))) 

HIIG_plot = HIIG_plot.set_index(r"geo\time").T
HIIG_plot.drop(['EU','EA18'], axis=1, inplace=True)

#	CP-HIS	HICP - Total services

HIS_plot = eurostat_columns_df(HICP, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['CP-HIS'], "unit": ["HICP2015"], r"geo\time": []})
HIS_plot = HIS_plot.drop(['indic','unit', 's_adj'], axis=1).reset_index(drop = True)

for geo in HIS_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        HIS_plot.at[HIS_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]


countries_aggr.append(list(HIS_plot[r"geo\time"])) 

HIS_plot = HIS_plot.set_index(r"geo\time").T

#   CP-HI00XEF	HICP - All items excluding energy, food, alcohol and tobacco

HI00XEF_plot = eurostat_columns_df(HICP, start_date, end_date, dict_col = { "s_adj": ['NSA'], "indic": ['CP-HI00XEF'], "unit": ["HICP2015"], r"geo\time": []})
HI00XEF_plot = HI00XEF_plot.drop(['indic','unit', 's_adj'], axis=1).reset_index(drop = True)

for geo in HI00XEF_plot[r"geo\time"]:
    if geo in set(ISO['alpha-2']):
        HI00XEF_plot.at[HI00XEF_plot[r"geo\time"] == geo,r"geo\time"] = ISO.loc[ISO['alpha-2'] == geo,'name'].iloc[0]


countries_aggr.append(list(HI00XEF_plot[r"geo\time"])) 

HI00XEF_plot = HI00XEF_plot.set_index(r"geo\time").T

#union list of countries
countries = countries_aggr[0]
for icountries in countries_aggr:
    countries = list_union(countries, icountries)
countries.sort()
#print(len(countries),countries)

countries_diff = []
for icountries in countries_aggr:
    countries_diff.append(list_diff(countries, icountries))

#for icountries in countries_diff:
#    print(icountries)

for country in countries_diff[1]:
    HI00_plot[country ] = np.nan
for country in countries_diff[2]:
    HU_plot[country ] = np.nan
for country in countries_diff[3]:
    job_plot[country ] = np.nan
for country in countries_diff[4]:
    SI_Construction_plot[country ] = np.nan
for country in countries_diff[5]:
    SI_Economic_plot[country ] = np.nan
for country in countries_diff[6]:
    SI_Industrial_plot[country ] = np.nan
for country in countries_diff[7]:
    SI_Retail_plot[country ] = np.nan
for country in countries_diff[8]:
    SI_Consumer_plot[country ] = np.nan
for country in countries_diff[9]:
    SI_Services_plot[country ] = np.nan
for country in countries_diff[10]:
    RS_plot[country ] = np.nan
for country in countries_diff[11]:
    SV_plot[country ] = np.nan
for country in countries_diff[12]:
    CN_plot[country ] = np.nan
for country in countries_diff[13]:
    IRST_LTGBY_plot[country ] = np.nan
for country in countries_diff[14]:
    IND_plot[country ] = np.nan
for country in countries_diff[15]:
    CSTR_plot[country ] = np.nan
for country in countries_diff[16]:
    PEL_plot[country ] = np.nan
for country in countries_diff[17]:
    IRST_DDI_plot[country ] = np.nan
for country in countries_diff[18]:
    IRST_3M_plot[country ] = np.nan
for country in countries_diff[19]:
    grossVA_plot[country ] = np.nan
for country in countries_diff[20]:
    employment_plot[country ] = np.nan
for country in countries_diff[21]:
    CEL_plot[country ] = np.nan
for country in countries_diff[22]:
    IEL_plot[country ] = np.nan
for country in countries_diff[23]:
    PNG_plot[country ] = np.nan
for country in countries_diff[24]:
    CNG_plot[country ] = np.nan
for country in countries_diff[25]:
    ING_plot[country ] = np.nan
for country in countries_diff[23]:
    HIIG_plot[country ] = np.nan
for country in countries_diff[24]:
    HIS_plot[country ] = np.nan
for country in countries_diff[25]:
    HI00XEF_plot[country ] = np.nan

#store the pickles for all the df needed
dataframe_list = [
    [GDP_card,'GDP_card'],
    [HICP_card,'HICP_card'],
    [HU_card,'HU_card'],
    [BC_card,'BC_card'],
    [GDP_plot,'GDP_plot'],
    [countries,'countries'],
    [HI00_plot,'HI00_plot'],
    [HU_plot,'HU_plot'],   
    [job_plot,'job_plot'],   
    [SI_Construction_plot,'SI_Construction_plot'],   
    [RS_plot,'RS_plot'],   
    [SV_plot,'SV_plot'],   
    [CN_plot,'CN_plot'],   
    [IRST_LTGBY_plot,'IRST_LTGBY_plot'],   
    [IND_plot,'IND_plot'],   
    [CSTR_plot,'CSTR_plot'],   
    [PEL_plot,'PEL_plot'],   
    [SI_Economic_plot,'SI_Economic_plot'],   
    [SI_Industrial_plot,'SI_Industrial_plot'],   
    [SI_Retail_plot,'SI_Retail_plot'],   
    [SI_Consumer_plot,'SI_Consumer_plot'],   
    [SI_Services_plot,'SI_Services_plot'],   
    [IRST_DDI_plot,'IRST_DDI_plot'],   
    [IRST_3M_plot,'IRST_3M_plot'],   
    [grossVA_plot,'grossVA_plot'],   
    [employment_plot,'employment_plot'],   
    [CEL_plot,'CEL_plot'],   
    [IEL_plot,'IEL_plot'],   
    [PNG_plot,'PNG_plot'],   
    [CNG_plot,'CNG_plot'],   
    [ING_plot,'ING_plot'],   
    [HIIG_plot,'HIIG_plot'],
    [HIS_plot,'HIS_plot'],
    [HI00XEF_plot,'HI00XEF_plot'],

]


for dataframe, name in dataframe_list:
    picklify(dataframe, name)
