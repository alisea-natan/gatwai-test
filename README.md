## Main Installation Recommendation
To activate a virtual environment (venv) and install dependencies from a `requirements.txt` file, follow these instructions:      
1. Create a virtual environment (optional):
   - Open a terminal or command prompt.
   - Navigate to the project folder.
   - Execute the command: `python3 -m venv myenv`
   - Replace `myenv` with the name you want to give to your virtual environment.

2. Activate the virtual environment:
   - On Windows:
     - Execute the command: `myenv\Scripts\activate.bat`
   - On macOS and Linux:
     - Execute the command: `source myenv/bin/activate`

3. Install dependencies from `requirements.txt`:
   - With the virtual environment activated, execute the command: `pip3 install -r requirements.txt`
   - This will install all the required packages and their specified versions into the virtual environment.

Note: Make sure you have Python installed on your system before creating a virtual environment. The steps above assume that you have Python and pip (Python package manager) properly set up.     
This project was created with Python 3.10.

## Tasks

### Task 1: 
**Description:**    
You are the owner of an ice cream business, and you want to develop a model that can predict the daily revenue in dollars based on the ambient air temperature (in degrees Celsius).Your database: https://drive.google.com/file/d/1BmjSO1RgKdD_L7r-oYPTB7jYnngqfKv7/view?usp=sharing      

**Files:**     
Input: `data/IceCreamData.csv`    
Analysis: `Task1.ipynb`    
Code: `icecream_daily_revenue_task1.py`    
Output: `linear_regression_model.pkl`    

**Notes:**      
For this task was created Jupyter Notebook file `Task1.ipynb` that shows data distribution and compares ML and non-ML method.
Was chosen Linear Regression and final model was saved to file `linear_regression _model.pkl`.

**Usage:**
- Run command `python3 icecream_daily_revenue_task1.py` will generate for you file with saved model.
- For the current moment if client want new prediction, he can put temperature into `icecream_revenue_prediction()` function and receive revenue.

**Output:**

Without new temperature value:

    The model has been saved to linear_regression_model.pkl.
With new temperature value:

    The model has been saved to linear_regression_model.pkl.
    Expected revenue: 259.2675221973662

### Task 2: 
**Description:**    
Get the current weather in Kyiv and make a forecast for the next 10 days. Use Open Weather Map for this task (https://openweathermap.org/). 

**Files:**
Code: `weather_forecast_task2.py`    

**Notes:**  
For this task you will need API key from mentioned site.
One existing problem is that Open Weather Map provides forecasting info for more than 8 days only with paid subscription.
So for the current moment output will show you current weather and forecasting with period of 3 hours, not 1 day.

**Usage:**
- Create .env file and add line to it: WEATHER_API="KEY" , where KEY is your API key from https://openweathermap.org/ .
- Run command `python3 weather_forecast_task2.py`

**Output:**

    Current Weather in Kyiv:
    Temperature: 300.13 K
    Weather Description: light rain
    
    10-times Weather Forecast for Kyiv:
    Date: 2023-07-03 18:00:00
    Temperature: 301.2 K
    Weather Description: light rain
    ---
    Date: 2023-07-03 21:00:00
    Temperature: 297.67 K
    Weather Description: broken clouds
    ---
    Date: 2023-07-04 00:00:00
    Temperature: 292.15 K
    Weather Description: clear sky
    ---
    Date: 2023-07-04 03:00:00
    Temperature: 290.65 K
    Weather Description: clear sky
    ---
    Date: 2023-07-04 06:00:00
    Temperature: 290.33 K
    Weather Description: clear sky
    ---
    Date: 2023-07-04 09:00:00
    Temperature: 296.46 K
    Weather Description: scattered clouds
    ---
    Date: 2023-07-04 12:00:00
    Temperature: 301.19 K
    Weather Description: clear sky
    ---
    Date: 2023-07-04 15:00:00
    Temperature: 302.41 K
    Weather Description: few clouds
    ---
    Date: 2023-07-04 18:00:00
    Temperature: 301.79 K
    Weather Description: overcast clouds
    ---
    Date: 2023-07-04 21:00:00
    Temperature: 297.27 K
    Weather Description: overcast clouds
    ---

### Task 3: Forecasting of the personnel department  
**Description:**    
Determine the number of employees who left the company and who are working
Which technology contributes the most to predicting the target indicator?
Predicting employees who may leave the company.
Database: https://drive.google.com/file/d/1WHnsmG9crcL6demy683yHSa-FFofNSa1/view?usp=sharing

**Files:**     
Input: `data/HR.csv`     
Code: `hr_research_task3.py`    

**Notes:**     
As dataset is imbalanced, there would be better to use _imbalanced-learn_ library. 
Model chosen for that calculations is Random Forest Classifier with default parameters.
Random Forest is proven best for such cases.

Feature importance shows us the most important factors because of which people left this company.

Next part of output shows 10 id of workers that did not leave but have higher probability to do that.

**Usage:**
- Run command `python3 hr_research_task3.py`

**Output:**

    Number of employees who left the company: 3571
    Number of employees who are still working: 11428
    
    Higher Feature Importances:
                    feature  importance
    0    satisfaction_level    0.303612
    2        number_project    0.180235
    4    time_spend_company    0.178823
    3  average_montly_hours    0.162288
    1       last_evaluation    0.126009
    
    Higher probabilities to leave:
           Probabilities
    7762            0.38
    6263            0.38
    9781            0.36
    10098           0.33
    7989            0.33
    3780            0.32
    5847            0.32
    7077            0.30
    6358            0.30
    2415            0.29

### Task 4: 
**Description:**     
A command-line tool that gets the city name and returns the current weather forecast. Open Weather Map API (https://openweathermap.org/) is used to obtain weather data and analyze it

**Files:**     
Code: `city_temperature_task4.py`    

**Notes:** 
For CLI was used _click_ package instead of built-in _argparse_ as it makes code more readable and supports a lot of useful features for improving such task in the future.
Solution designed for 2 ways of usage - with personal API key of each customer or with built-in API key

**Usage:**
- For using built-in API key create .env file and add line to it: WEATHER_API="KEY" , where KEY is your API key from https://openweathermap.org/ .
- Run command `python3 city_temperature_task4.py Kyiv`


- For using customers API key run command `python3 city_temperature_task4.py Kyiv --api-key "KEY"`, where KEY is your API key from https://openweathermap.org/ .

**Output**

    Weather in Kyiv:
    Temperature: 300.13 K
    Weather Description: light rain

### Task 5: 
**Description:**     
In this task, you need to include the prediction of the next match, in which the options (win, draw, or loss) are possible. Use this website https://sportsdata.io/ 

**Files:**       
Analysis: `Task5.ipynb`    
Code: `match_prediction_task5.py`   
Output: `game5.csv`, `teams5.csv`, `to_predict.csv`    

**Notes:** 
For this challenging task I choose LoL sport matches. 
Output csv files were made for 2 purposes - to work offline as this free API key is not endless, and to work easier in Jupyter Notebook, to faster check best classifier to this task.
Updates that could be added:
1. More offline - write nit only in Jupyter Notebook, but also in main code usage of csv files if api is unavailable (free API key from them have his own limit per day).
2. More info - here prediction was received using Random Forest Classifier only on data about teams wins and loses etc. for this season. Another data that I found useful is players statistics, but it would be not 1-day solution.
3. More documentation and structure - it would be easier to work if just move all this data to any DB and have schema of this data.
4. Simpler calculations - if we want to use only such statistics, then we could find out simple formula and calculate success faster and without receiving of all dataset each time.

So, current results are not so good, probability of success is about 50%, just as tossing a coin, but with current data and time, I think, it shows possibilities and problems of this project really good.

**Usage**   
- Run command `python3 match_prediction_task5.py`

**Output**

    Draw

or

    Team {team_name} will win.
