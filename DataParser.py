import requests
import csv
# import pprint

# Open data description
with open('data/description/region.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader, None)
    regions = list(reader)


url = "https://declarator.org/api/v1/search/sections/"
years = ['2012', '2013', '2014', '2015', '2016', '2017']
counts = []
average_incomes = []

for year in years:
    for region in regions:
        incomes = []
        params = {'region': region[0], 'year': year}
        response = requests.get(url, params=params).json()
        count = response["count"]
        counts.append(count)
        print("%s: %d" % (region[1], count))
        reduced = response["results"]
        if count > 0:
            for entry in reduced:
                income = entry["incomes"][0]["size"]
                incomes.append(income)
            average_incomes.append(incomes)
            print(average_incomes)
        else:
            average_incomes.append("")
