import pandas as pd


# Rows are years
# Columns are different event types
def createQuestion2DataModel(df: pd.DataFrame):
    print("yes")
    print(df['Event Type Group'].value_counts())
    print("no")
    list_of_years = df['Year'].unique().tolist()
    print(list_of_years)
    list_of_years.sort()
    print(list_of_years)


    # data = pd[dict(out["Assault"])]
    # print(data)

if __name__ == '__main__':
    filename = "data/cleaned_output.csv"
    df = pd.read_csv(filename)

    createQuestion2DataModel(df)
