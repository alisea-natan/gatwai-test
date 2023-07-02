import pandas as pd
from sklearn.linear_model import LinearRegression
from os.path import join
import pickle


def icecream_revenue_prediction():
    df = pd.read_csv(join('data', 'IceCreamData.csv'))

    X = df[['Temperature']]
    y = df['Revenue']

    # You can find plot and comparison between simple multiplier and linear regression in the Task1.ipynb
    model = LinearRegression()

    model.fit(X, y)

    filename = 'linear_regression_model.pkl'
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

    print(f"The model has been saved to {filename}.")


if __name__ == "__main__":
    icecream_revenue_prediction()
