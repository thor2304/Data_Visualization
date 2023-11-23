import pandas
import clean_counties


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

    df = pandas.read_csv('../data/Major_Safety_Events.csv', low_memory=False)

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
    df.to_csv("../data/cleaned_output.csv", mode="w", encoding="utf8")


def cap_column(df, column_name, cap):
    df.loc[df[column_name] > cap, column_name] = cap
    return df


if __name__ == '__main__':
    main()
    clean_counties.clean_populations()
