import pandas


def main():
    # read one line at a time from the csv file
    # for each line remove the first comma
    file = open("../population-raw-data/county-pop-2019.csv", "r")
    new_file = open("../population-raw-data/cleaned-county-pop.csv", "w")
    i = 0
    while True:
        line = file.readline()
        if not line:
            break

        if i == 0:
            newline = "ID,2014,2015,2016,2017,2018,2019\n"
            new_file.write(newline)
            i += 1
            continue

        # Remove first comma from line
        newline = line[0:2] + line[3:]

        new_file.write(newline)
        i += 1


    file.close()
    new_file.close()


def add2020_2022():
    file2014_2019 = pandas.read_csv('../population-raw-data/cleaned-county-pop.csv', low_memory=False, dtype=str)
    file2020_2022 = pandas.read_csv('../population-raw-data/county-pop-2022.csv', low_memory=False, dtype=str)

    # Columns to add from 2020-2022
    print(file2014_2019.columns)
    print(file2020_2022.columns)
    columns_indexes_to_add = [2, 3, 4]

    # last index in file2019
    lastIndex = len(file2014_2019.columns)

    for index in columns_indexes_to_add:
        file2014_2019.insert(lastIndex, file2020_2022.columns[index], file2020_2022[file2020_2022.columns[index]])
        lastIndex += 1

    print(file2014_2019.columns)

    file2014_2019.to_csv('../data/counties-population-2014-2022.csv', index=False)


if __name__ == '__main__':
    main()
    add2020_2022()
