import numpy as np
import pandas as pd
from datetime import datetime
from itertools import product
from pathlib import Path
import eurostat

start_date = 1900
end_date = 2022

def write_log(str):
    '''
    function used to write on the log.txt file the date and time and notes on the changes while updating the /input csv files
    '''
    # datetime object containing current date and time
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    log_file = open('log.txt', 'a')
    log_file.write(f'[{now}] {str}\n')
    log_file.close()

def list_diff(li1, li2): 
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2] 
    return li_dif 

def list_union(lst1, lst2): 
    final_list = list(set(lst1) | set(lst2)) 
    return final_list 

def eurostat_columns_df(df, start_date, end_date, dict_col):
    '''
    Return a filtered dataframe based on the filters given as arguments. Currently used to filter dataframes dowloaded from Eurostat,
    but can be used also to filter other dataframes with a similar structure.
    
    df: DataFrame
        The original DataFrame that will be filtered.
    time_interval: str
        This can be either "Y" (yearly data), "Q" (quarterly data), "M" (monthly data). This string is used to match the different
        format used by Eurostat to assign column names.
        For the yearly data ("Y"), time columns follow the format "2020", "2019", etc..
        For the quarterly data ("Q"), time columns follow the format "2020Q1", ... , "2020Q4".
        For the montly data ("M"), time columns follow the format "2020M01", ... , "2020M12".
    start_date: int
        The year to consider as starting year for filtering the time columns in the DataFrame.
    end_date: int
        The year to consider as last year of data for filtering the time columns in the DataFrame.
    dict_col: dict
        Dictionary that includes as keys the name of the column(s) (other than the time columns) to maintain
        in the filtered DataFrame.
        A list should be assigned to each key, and it should contain the values for that column to maintain,
        for example, {"age": [16]} keeps the column age and the rows in the dataframe for which age == 16.
        An empty list can be passed to a column, for example, {"age": []}, to maintain the age column without
        filtering any row based on the values in that column.
    
    EXAMPLE:
    eurostat_columns_df(df, "Y", 2010, 2020, dict_col = {"sex": ["T"], "isced11": [], "age": [], "unit": [], r"geo\time": []})
    '''
    time_interval = str(df.columns[-1])
    years = [f"{x}" for x in range(start_date, end_date + 1)] # Create a list with the year of interest
    if len(time_interval) == 4: # If the DataFrame contains yearly data and the time columns follow the year format
        time_cols = [] # Initialize an empty list
        for year in years: # For each year (a column name)
            if year in list(df): # If that year is in the name of the columns of the DataFrame
                time_cols.append(year) # Append that year to the initalized list
    elif len(time_interval) == 6 and time_interval[4] == "Q": # If quarterly data
        quarters = ["Q1", "Q2", "Q3", "Q4"] # Create a list with the four strings that specify the quarter
        temp_product = product(years, quarters) # Combine all the years of interest with the quarters within a year
        temp_time = [] # Initialize an empty list
        for i in temp_product: # Loop over the tuples generate by the product
            temp_time.append("".join(i)) # Join the elements in each tuple to obtain the desired format, for example, "2020Q1" 
        time_cols = [] # Initialize an empty list
        for quarter in temp_time: # For each quarter of interest
            if quarter in list(df): # Check if it is in the list of columns of the Dataframe
                time_cols.append(quarter) # If there is a match append it to the initialized list of column names
    elif len(time_interval) == 7 and time_interval[4] == "M": # If monthly data
        months = ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12"] # Create a list with the twelve strings that specify the month
        temp_product = product(years, months) # Combine all the years of interest with the months within a year
        temp_time = [] # Initialize an empty list
        for i in temp_product: # Loop over the tuples generate by the product
            temp_time.append("".join(i)) # Join the elements in each tuple to obtain the desired format, for example, "2020M1" 
        time_cols = [] # Initialize an empty list
        for month in temp_time: # For each month of interest
            if month in list(df): # Check if it is in the list of columns of the Dataframe
                time_cols.append(month) # If there is a match append it to the initialized list of column names
    new_cols = [] # Initialize a list for the names of the columns in the filtered DataFrame
    temp_df = df.copy() # Create a copy of the initial DataFrame
    for arg in dict_col: # Iterate over the keys (name of columns) in the dictionary
        if arg in list(df): # If the key matches the name of one of the columns
            if dict_col[arg]: # If the list associated to the key in the dictionary is non-empty
                temp_df = temp_df[temp_df[arg].isin(dict_col[arg])] # Slice the DataFrame to maintain only the rows with values for that column matching the list given
                new_cols.append(arg) # Then append the name of the column to the new names
            else: # If the list is empty
                new_cols.append(arg) # Just append the name of the column since the DataFrame should not be sliced using values in this column
    new_cols += time_cols # Add to the list of columns the name of the time columns to maintain in the new DataFrame
    temp_df = temp_df[new_cols] # Slice the DataFrame to maintain only the selected columns
    return temp_df

def eurostat_requests(path,dict_codes):
    '''
    Function to request data from Eurostat using variable codes from a dictionary. Then writes the data to csv.
    '''
    for value in dict_codes: # For each variable in the dictionary (key) get the associated Eurostat code for the request
        df = eurostat.get_data_df(dict_codes[value]) # Assign the dataframe returned from the request to the variable (key) of the dictionary
        # slice large datasets
        if value == 'Gross_value_added_and_income_by_industry':
            df = df.drop(df[(df["s_adj"] != "NSA") | (df["na_item"] != "B1G") | (df["unit"] != "CLV_I05") | (df["nace_r2"] != "TOTAL")].index)
        elif value == 'GDP_and_main_components':
            df = df.drop(df[(df["na_item"] != "B1GQ") | (df["unit"] != "CLV_I05")].index)
        elif value == 'Harmonized_index_of_consumer_prices_monthly_data':
            df = df.drop(df[(df["s_adj"] != "NSA") | (df["indic"] != "CP-HI00") | (df["unit"] != "HICP2015")].index)
        elif value == 'Employmentby_industry':
            df = df.drop(df[(df["s_adj"] != "SCA") | (df["na_item"] != "EMP_DC") | (df["unit"] != "PCH_PRE_PER") | (df["nace_r2"] != "TOTAL")].index)
        elif value == 'Unemployment_by_sex_and_age_monthly_data':
            df = df.drop(df[(df["s_adj"] != "SA") | (df["sex"] != "T") | (df["unit"] != "PC_ACT") | (df["age"] != "TOTAL")].index)

        path_file = path / f"{value}.csv" # Define the path to th file
        df.to_csv(path_file, index = False) # Write the dataframe to csv

