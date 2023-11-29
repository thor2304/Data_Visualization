import pandas as pd


# Rows are years
# Columns are different event types
def createQuestion2DataModel(df: pd.DataFrame):
    y_akse = pd.DataFrame()

    temp_data = df['Event Type Group'].value_counts().sort_index()

    print(temp_data)
    # Delete row
    temp_data.drop('Non-RGX Collision', inplace=True)
    print(temp_data)

    y_akse['Event Type Group'] = temp_data.values

    x_akse = df['Event Type Group'].unique()
    x_akse.sort()

if __name__ == '__main__':
    filename = "data/cleaned_output.csv"
    df = pd.read_csv(filename)

    createQuestion2DataModel(df)
