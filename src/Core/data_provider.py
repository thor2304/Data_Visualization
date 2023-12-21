import os
import pandas as pd
import numpy as np
import united_states

df = None


def get_df():
    global df
    if df is not None:
        return df
    if os.environ["fetch"] == "True":
        print("fetch data")
        df = pd.read_csv('http://datadump.cryptobot.dk/Major_Safety_Events.csv', low_memory=False)
    else:
        filename = f"{__file__[:-(4 + 1 + 8 + 3)]}data/cleaned_output.csv"
        df = pd.read_csv(filename)
        # df.apply(lambda x: x['Event Date'].format(name=x['name']), axis=1)
        df['Event Date'] = pd.to_datetime(df['Event Date'])
        df['Event Time'] = pd.to_datetime(df['Event Time'])

    # print("data fetched")
    # print(df.columns[12])
    # print(df["Event Time"])

    return df


category_orders = None
reverse_category_orders = None


def get_category_orders() -> dict:
    global category_orders
    if category_orders is not None:
        return category_orders
    category_orders = {"Event Type Group": sorted(get_df()["Event Type Group"].unique())}
    return category_orders


def get_reverse_category_orders() -> dict:
    global reverse_category_orders
    if reverse_category_orders is not None:
        return reverse_category_orders
    reverse_category_orders = {"Event Type Group": sorted(get_df()["Event Type Group"].unique(), reverse=True)}
    return reverse_category_orders

