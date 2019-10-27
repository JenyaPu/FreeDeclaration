import requests
import csv
import sqlite3
from time import gmtime, strftime
import time
import datetime
# import statistics
# import pprint

start_from = 0
table = "income"


def get_single_region_data_incomes(region):

    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    year_data = []
    counts = []

    for year in years:
        total = []
        incomes = []
        params = {'region': region[0], 'year': year, 'page': 1}
        response = requests.get(url, params=params).json()
        count = response["count"]
        counts.append(count)
        print("%s в %s: %d" % (region[1], year, count))
        pages = count // 10 + 1
        if count > 0:
            for i in range(1, pages):
                params = {'region': region[0], 'year': year, 'page': i}
                response = requests.get(url, params=params).json()
                reduced = response["results"]
                for entry in reduced:
                    if len(entry["incomes"]) > 0:
                        income = entry["incomes"][0]["size"]
                        incomes.append(income)
                total.append(incomes)
        else:
            total.append("")
        print(total)
        if len(total) > 0:
            if len(total[0]) > 0:
                total_strings = str(total[0][0])
                for k in range(1, len(total[0])):
                    total_strings = total_strings + " " + str(total[0][k])
            else:
                total_strings = ""
        else:
            total_strings = ""

        year_data.append(count)
        year_data.append(total_strings)
    array = [region[0], region[1], year_data[0], year_data[1], year_data[2], year_data[3], year_data[4],
             year_data[5], year_data[6], year_data[7], year_data[8], year_data[9], year_data[10], year_data[11],
             timestamp]
    return array


def get_single_region_data_real_estates(region):

    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    year_data = []
    counts = []

    for year in years:
        total = []
        incomes = []
        params = {'region': region[0], 'year': year, 'page': 1}
        response = requests.get(url, params=params).json()
        count = response["count"]
        counts.append(count)
        print("%s в %s: %d" % (region[1], year, count))
        pages = count // 10 + 1
        if count > 0:
            for i in range(1, pages):
                params = {'region': region[0], 'year': year, 'page': i}
                response = requests.get(url, params=params).json()
                reduced = response["results"]
                for entry in reduced:
                    if len(entry["real_estates"]) > 0:
                        all_together = 0
                        for estate in entry["real_estates"]:
                            squares = estate["square"]
                            if squares is not None:
                                all_together = all_together + squares
                            incomes.append(str(round(all_together, 1)) + " ")
                total.append(incomes)
        else:
            total.append("")
        print(total)
        if len(total) > 0:
            if len(total[0]) > 0:
                total_strings = str(total[0][0])
                for k in range(1, len(total[0])):
                    total_strings = total_strings + " " + str(total[0][k])
            else:
                total_strings = ""
        else:
            total_strings = ""

        year_data.append(count)
        year_data.append(total_strings)
    array = [region[0], region[1], year_data[0], year_data[1], year_data[2], year_data[3], year_data[4],
             year_data[5], year_data[6], year_data[7], year_data[8], year_data[9], year_data[10], year_data[11],
             timestamp]
    return array


def add_single_region_data_persons(region, conn, cursor):

    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    for year in years:
        params = {'region': region[0], 'year': year, 'page': 1}
        response = requests.get(url, params=params).json()
        count = response["count"]
        print("%s в %s: %d" % (region[1], year, count))
        pages = count // 10 + 1
        if count > 0:
            for i in range(1, pages):
                params = {'region': region[0], 'year': year, 'page': i}
                response = requests.get(url, params=params).json()
                reduced = response["results"]
                for entry in reduced:
                    if (len(entry["real_estates"]) > 0) and (len(entry["incomes"]) > 0) \
                            and (len(entry["main"]["person"]) > 0) and (len(entry["main"]["office"]) > 0):
                        decl_id = entry["main"]["person"]["id"]
                        name = entry["main"]["person"]["name"]
                        gender = entry["main"]["person"]["gender"]
                        office = entry["main"]["office"]["name"]
                        if entry["main"]["party"] is not None:
                            party = entry["main"]["party"]["name"]
                        else:
                            party = ""
                        income = entry["incomes"][0]["size"]
                        squares = 0
                        squares2 = 0
                        for estate in entry["real_estates"]:
                            square = estate["square"]
                            if square is not None:
                                if estate["type"]["id"] != 1:
                                    squares = squares + square
                                elif estate["type"]["id"] == 1:
                                    squares2 = squares2 + square
                        squares = round(squares, 1)
                        array = [decl_id, region[0], region[1], year, name, gender, office, party,
                                 income, squares, squares2, timestamp]
                        cursor.execute("INSERT OR IGNORE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                                       array)
                        conn.commit()


def initialize_databases():

    conn1 = sqlite3.connect("data/database/incomes.db")
    cursor = conn1.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS incomes
                      (region_id text primary key, region text, 
                      count_2012 text, incomes_2012 text, count_2013 text, incomes_2013 text,
                      count_2014 text, incomes_2014 text, count_2015 text, incomes_2015 text,
                      count_2016 text, incomes_2016 text, count_2017 text, incomes_2017 text,
                      timestamp text)
                   """)
    conn1.commit()
    cursor.close()
    conn1.close()

    conn2 = sqlite3.connect("data/database/real_estates.db")
    cursor = conn2.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS real_estates
                      (region_id text primary key, region text, 
                      count_2012 text, real_estate_2012 text, count_2013 text, real_estate_2013 text,
                      count_2014 text, real_estate_2014 text, count_2015 text, real_estate_2015 text,
                      count_2016 text, real_estate_2016 text, count_2017 text, real_estate_2017 text,
                      timestamp text)
                   """)
    conn2.commit()
    cursor.close()
    conn2.close()

    conn3 = sqlite3.connect("data/database/persons.db")
    cursor = conn3.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS persons
                      (decl_id text primary key, region_id text, region text, year text, name text, gender text,
                      office text, party text, income text, squares text, squares2 text, timestamp text)
                   """)
    conn3.commit()
    cursor.close()
    conn3.close()


def download_incomes():
    conn = sqlite3.connect("data/database/incomes.db")
    cursor = conn.cursor()
    for j in range(start_from, len(regions)):
        region_take = regions[j]
        income_data = get_single_region_data_incomes(region_take)
        cursor.execute("INSERT OR IGNORE INTO incomes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", income_data)
        conn.commit()
    cursor.close()
    conn.close()


def download_real_estates():
    conn = sqlite3.connect("data/database/real_estates.db")
    cursor = conn.cursor()
    for j in range(start_from, len(regions)):
        region_take = regions[j]
        income_data = get_single_region_data_real_estates(region_take)
        cursor.execute("INSERT OR IGNORE INTO real_estates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", income_data)
        conn.commit()
    cursor.close()
    conn.close()


def download_people():
    conn = sqlite3.connect("data/database/persons.db")
    cursor = conn.cursor()
    for j in range(start_from, len(regions)):
        region_take = regions[j]
        add_single_region_data_persons(region_take, conn, cursor)


# Open region description
with open('data/description/region.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader, None)
    regions = list(reader)
url = "https://declarator.org/api/v1/search/sections/"
years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']

initialize_databases()
start = time.time()
download_incomes()
download_real_estates()
download_people()
end = time.time()
print(str(datetime.timedelta(seconds=(end - start))))
