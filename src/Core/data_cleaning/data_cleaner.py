import pandas as pd
import clean_counties

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))


def write_cleaned(filepath: str):
    indexes = (0, 1)

    with open(filepath, 'r', encoding="utf8") as input_file:
        with open("../data/cleaned_output.csv", "w", encoding="utf8") as output_file:
            while True:
                line = input_file.readline()
                if not line:
                    break
                # end of file reached

                if line == "\n":
                    continue

                line = line.split(",")

                # print(line)
                out = line[indexes[0]]

                for index in indexes[1:]:
                    try:
                        out += "," + line[index]
                        # print(f"line was succesful {line}")
                    except IndexError:
                        print(index)
                        print(line)

                output_file.write(out + "\n")


def main():
    column_contents = {}

    # Index 20: Runaway train flag -> remove column (present on 48 rows)
    # Index 24: Property damage type -> remove column (present on ~2000 rows)
    # Index 35: LatLon -> keep column, missing on 11616 rows (transform missing rows or drop them if we need latlon) If we dont need the coordinates drop column
    # Index 39: HazMat -> drop column (not present at all) drop HazMat Type description as well (column 40)
    # Index 40: HazMat Type description -> drop column (not present at all)
    # Index 43: Other Fire Fuel Description -> drop column (present on 3 rows)
    # Index 46: Current conditions 'Fast current': 5, 'Flat water (no current)': 1, 'Meduim current': 2, 'Slow current': 4 -> drop column (present on 12 rows)
    # Index 47: Tide 'Low tide': 3, 'Slack tide': 4, 'High tide': 4, 'Non-tidal waters': 1 -> drop column (present on 12 rows)
    # Index 55: 'No control device': 6, 'Passive device: pavement markings': 6, 'Active device: traffic signal': 7, 'Passive device: do not pass': 1, 'Passive device: stop sign': 1 -> drop column (present on 21 rows)

    index = 33

    df = pd.read_csv('../data/Major_Safety_Events.csv', low_memory=False)

    df['Event Date'] = pd.to_datetime(df['Event Date'])
    df['Event Time'] = pd.to_datetime(df['Event Time'])

    column_indexes_to_drop = [20, 24, 35, 39, 40, 43, 46, 47, 55]
    column_names_to_drop = []

    for row in df.iterrows():
        for ind in column_indexes_to_drop:
            # print(row[1].keys()[ind])
            column_names_to_drop.append(row[1].keys()[ind])
        break

    print("dropping columns")
    for name in column_names_to_drop:
        df.pop(name)

    # Drop rows where Year is 2023
    df = df[df['Year'] != 2023]

    df = add_month_column(df)
    df = add_state_column(df)
    df = add_event_divided_by_citizens(df)

    # print(df.info())
    for row in df.iterrows():
        # print(row[1].iloc[20])
        rowRead = row[1].iloc[index]
        rowRead = row[1]["Vehicle Speed"]
        if column_contents.get(rowRead) is None:
            column_contents[rowRead] = 1
        else:
            column_contents[rowRead] += 1
    # write_cleaned("Major_Safety_Events.csv")
    pass

    # print(column_contents)
    high_keys = filter(lambda x: x > 20, column_contents.keys())

    for key in high_keys:
        print(f"{key}: {column_contents[key]}")

    df = cap_column(df, "Vehicle Speed", 200)

    print(df)

    df.to_csv("../data/cleaned_output.csv", mode="w", encoding="utf8")


def cap_column(df, column_name, cap):
    df.loc[df[column_name] > cap, column_name] = cap
    return df


def add_month_column(df: pd.DataFrame):
    for index, row in df.iterrows():
        df.at[index, 'Month'] = row['Event Date'].month_name()
    return df


# This method is dependent on add_state_column
def add_event_divided_by_citizens(df: pd.DataFrame):
    state_population = pd.read_csv(f"../data/states-population.csv")

    for index, row in df.iterrows():
        print(f"index: {index}")
        state = row['State']
        if state == "Unknown" or state == "Puerto Rico":
            continue
        year = row['Year']
        population = state_population.loc[state_population['Years'] == str(state), str(year)].values[0]
        df.at[index, 'Event Per Mil Citizens'] = 1000000 / population
    return df


def add_state_column(df: pd.DataFrame):
    print("Adding state column")
    agencies = pd.read_csv(f"../data/agencies.csv", encoding="UTF-8", sep=";")
    data = pd.DataFrame()
    data['NTD ID'] = agencies['NTD ID']
    data['State'] = agencies['State']

    for index, row in df.iterrows():
        print(f"index: {index}")
        agency_id = row['NTD ID']
        results = data.loc[data['NTD ID'] == str(agency_id)]
        if len(results) == 0:
            df.at[index, 'State'] = "Unknown"
        else:
            df.at[index, 'State'] = abbrev_to_us_state[results.iloc[0]['State']]

    # Use df.map instead of the for loop
    # The input value for the key should be converted to string
    # The output value should be converted to a list
    # df['State'] = df['NTD ID'].map(lambda x: abbrev_to_us_state[data.loc[data['NTD ID'] == str(x)].iloc[0]['State']])

    return df


if __name__ == '__main__':
    main()
    clean_counties.clean_populations()
