import numpy as np

def growth_rate(data, window):
    '''
    Compute the moving average for the grow rate plots
    input: 
    dataframe containing the information for each country for each date
    # of days 
    output:
    dataframe containing the growth rate for each country for each date
    '''
    df_sub = data.copy()
    df_sub = df_sub.apply(lambda x: x - x.shift(periods = 1))
    df_sub.iloc[0] = data.iloc[0]
    df_GR = df_sub.copy()
    temp_data = data.copy()
    for country in list(df_GR):
        temp_data[country] = temp_data[country].replace(0, np.nan)
        df_GR[country] = (df_GR[country]/temp_data[country].shift(periods = 1))
        df_GR[country] = df_GR[country].rolling(window).mean()
    return df_GR

def ticks_log(df, selected_countries):
    '''
    Used to adjust the max tick (y-axis) for the plots with logarithmic scale
    input: 
    dataframe containing the information for each country for each date
    list of countries 
    output:
    list of values for the ticks of y axis
    list of strings for the ticks of y axis
    '''
    temp_max = 0
    label_max = []
    text_label_max = []
    tick = 1
    for country in selected_countries:
        if temp_max < df[country].max():
            temp_max = df[country].max()
    while tick < temp_max*(0.50):
        label_max.append(tick)
        text_label_max.append(f'{tick:,}')
        tick *= 10
    label_max.append(temp_max)
    text_label_max.append(f'{temp_max:,}')
    return label_max, text_label_max
