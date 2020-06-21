# COVID-19 - World Dashboard App

*COVID-19 - World Dashboard App* is a Python project that brings together different statistics on COVID-19. This dashboard aims at being mobile friendly and easily embeddable e.g. on a website. This dashboard uses free open-source resources and the Python language.

## Dependencies

- flask
- pandas
- ...

## Installation and environment setup

1) Be sure to have pipenv installed globally on your environment, if not:
```
pip install pipenv
```    
2) Clone this repository. Unzip it. And change directory into it from your terminal:
```
cd dashboard-world
```
3) Then replicate the virtual environment with all its dependencies:
```
pipenv install
```    
4) After a while your virtual environment should be ready, activate it (if your machine hasn't already done that for you) with:
```
pipenv shell
```
5) To launch the App:
```
(dashboard-world) python app.py
```    
You can now visit the http://localhost:8050 address in your browser (the default Flask app should be listening at the port :8050, unless otherwise specified).

## App Structure

[![functions scheme](https://github.com/Learning-from-the-curve/dashboard-world/blob/master/functions_scheme.png)](https://github.com/Learning-from-the-curve/dashboard-world/blob/master/functions_scheme.png)

### app.py
The app.py file is the one used by Heroku to deploy the app. It takes the functions from layout which are used to generate the plots. There are also other functions stored in app_functions that are called by the layout script.

### df_process.py
df_process.py takes the functions written in process_functions.py to filter and adjust the data. It is executed twice per day to update the pickle files (that we store in the pickles_jar). Those files contain the dataframes that we use for the plots. Furthermore, it checks the consistency of the data in the input folder before using them for the plots.

### layout_functions.py
Contains the functions to draw the plots:
- gen_map(...): generate and plot the world map with the # of confirmed cases for each country as the Z parameter
- draw_singleCountry_Scatter(...): generate and plot a scatterplot for confirmed/deaths with linear or log scale for the selected countries
- draw_mortality_fatality(...): generate and plot a scatterplot for mortality rate/Share of infected population/Growth rate confirmed cases/Growth rate deaths with date or days scale for the selected countries
- draw_singleCountry_Epicurve(...): generate and plot a scatterplot for Epidemic curve and policy index for confirmed/deaths for the selected countries
- make_item(...): create the Accordion to click to show/hide the dropdown menu of the countries

### process_functions.py
Contains the functions to support the filtering done by df_process.py:
- write_log(...): used to write on the log.txt file the date and time and notes on the changes while updating the /input csv files
- center_date(...): function used for an apply method, updates row with the difference of # of days in place of the date
- adjust_names(...): Adjust and update countries' names
- aggregate_countries(...): Returns an updated dataframe with aggregated provinces and states in a country
- moving_average(...): Compute the moving average for the epidemic curves

### app_functions.py
Contains support functions for the layout_functions.py:
- growth_rate(...): Compute the moving average for the grow rate plots
- ticks_log(...): Used to adjust the max tick (y-axis) for the plots with logarithmic scale

### pickle_functions.py
The pickle functions are used by other scripts to store and load data in/from the pickles_jar.

## Usage

[![flowchart usage](https://github.com/Learning-from-the-curve/dashboard-world/blob/master/configuration_scheme.png)](https://github.com/Learning-from-the-curve/dashboard-world/blob/master/configuration_scheme.png)
 
## Contributors

This dashboard has been developed by Alessandro Gallina, Federico Gallina and Giorgio Pizzuto, with the help of Prof. Dr. Glenn Magerman for the plots to visualize in the app. We are also very grateful to other members of the Learning from the Curve team and for funding from the Special COVID-19 ULB grant.
