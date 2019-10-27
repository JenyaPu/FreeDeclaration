import sqlite3
import pandas as pd
import seaborn as sns
import csv
import matplotlib.pyplot as plt
import warnings
import statistics
from plot_grid_map import plot_grid_map
# import numpy as np
# import matplotlib
warnings.filterwarnings(action='once')


def preprocess_data_incomes():

    conn1 = sqlite3.connect("data/database/incomes.db")
    df_income = pd.read_sql_query("SELECT * FROM incomes", conn1)
    conn1.close()

    new_df = pd.DataFrame(columns=['region', 'incomes'])
    for index, row in df_income.iterrows():
        region1 = row['region']
        all_incomes = row['incomes_2017']
        all_incomes = all_incomes.split(" ")
        for income in all_incomes:
            if income != "":
                if 0 < float(income) < 100000000:
                    new_df = new_df.append({'region': region1, 'incomes': float(income)}, ignore_index=True)
                else:
                    print("This guy is strange %s", income)

    conn2 = sqlite3.connect('data/database/incomes_processed.db')
    new_df.to_sql(name='incomes', con=conn2)
    conn2.close()


def make_boxplots(year, dpi):
    conn1 = sqlite3.connect("data/database/persons.db")
    df11 = pd.read_sql_query("SELECT * FROM persons", conn1)
    df11['income'] = df11['income'].astype(float)/12
    df11 = df11.loc[df11['year'] == year]
    fig = plt.figure(figsize=(50, 9), dpi=dpi)
    fig.subplots_adjust(bottom=0.3)
    sns.boxplot(x='region', y='income', data=df11, notch=False)
    plt.ylabel('Среднемесячный доход, руб.')
    plt.xlabel('Регион России')

    def add_n_obs(df22, group_col, y):
        medians_dict = {grp[0]: grp[1][y].median() for grp in df22.groupby(group_col)}
        xticklabels = [x.get_text() for x in plt.gca().get_xticklabels()]
        n_obs = df22.groupby(group_col)[y].size().values
        for (x, xticklabel), n_ob in zip(enumerate(xticklabels), n_obs):
            plt.text(x, medians_dict[xticklabel]*1.01, "N: "+str(n_ob),
                     horizontalalignment='center', fontdict={'size': 12}, color='white')

    add_n_obs(df11, group_col='region', y='income')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=60)
    plt.title('Доход чиновников в различных регионах России на %s год, руб.' % year, fontsize=14)
    plt.savefig("images/boxplot_incomes.png", bbox_inches='tight')
    plt.show()


def scatter_plot(region, year, a_square1, a_income1):
    conn1 = sqlite3.connect("data/database/persons.db")
    df0 = pd.read_sql_query("SELECT * FROM persons", conn1)
    df0['income'] = df0['income'].astype(float)/12
    df0['squares'] = df0['squares'].astype(float)
    conn1.close()
    df11 = df0.loc[df0['region_id'] == region[0]]
    df22 = df11.loc[df0['year'] == year]
    df22.loc[df0['gender'] == 'M', 'gender'] = 'Мужчины'
    df22.loc[df0['gender'] == 'F', 'gender'] = 'Женщины'
    df22['gender'].replace([None], 'Не указано', inplace=True)
    df33 = pd.DataFrame({"income": [float(a_income1)], "squares": [float(a_square1)], "gender": ["Народ"]})
    df22 = df22.append(df33, ignore_index=True)
    print(df22)
    if len(df22) > 1:
        categories = ["Мужчины", "Женщины", "Не указано", "Народ"]
        # colors = [plt.cm.tab10(i/float(len(categories)-1)) for i in range(len(categories))]
        colors = ["red", "blue", "orange", "green"]

        fig = plt.figure(figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
        ax = fig.add_subplot(111)
        for k, category in enumerate(categories):
            ax.scatter(
                'income', 'squares', data=df22.loc[df22.gender == category, :],
                s=20, c=colors[k], label=str(category))
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.legend(fontsize=12)
        plt.xlabel('Среднемесячный доход, руб.')
        plt.ylabel('Общая площадь недвижимости, кв.м.')
        # ax2.text(a_income, a_square, 'народ')
        ax.set_title(str(
            "Доходы и площадь недвижимости в регионе: " + region[1] +
            " за " + year + " год"), fontsize=12)
        plt.savefig("images/scatterplots/" + region[0] + "_" + year + ".png", bbox_inches='tight')


def make_scatterplots():
    for k, region1 in enumerate(regions):
        if k > 0:
            for year_take1 in years:
                df11 = df_rosstat.loc[df_rosstat['id'] == region1[0]]
                year_cols1 = [col for col in df_rosstat.columns if year_take1 in col]
                scatter_plot(region1, year_take1, df11[year_cols1[0]], df11[year_cols1[1]])


def make_averaged_table():
    df_averaged = pd.DataFrame(columns=(
        "region_id", "region", "year", "a_income", "a_squares", "a_squares2", "a_cor", "b_income", "b_squares"))
    conn = sqlite3.connect("data/database/persons.db")
    df = pd.read_sql_query("SELECT * FROM persons", conn)
    df['income'] = df['income'].astype(float) / 12
    df['squares'] = df['squares'].astype(float)
    df['squares2'] = df['squares2'].astype(float)
    conn.close()
    year_take = '2015'
    for i, region in enumerate(regions):
        df1 = df.loc[df['region_id'] == region[0]]
        df2 = df1.loc[df['year'] == year_take]
        if len(df2) > 1:
            df_rosstat1 = df_rosstat.loc[df_rosstat['id'] == region[0]]
            year_cols = [col for col in df_rosstat.columns if year_take in col]
            a_income = round(statistics.mean(df2['income']))
            a_squares = round(statistics.mean(df2['squares']), 1)
            a_squares2 = round(statistics.mean(df2['squares2']), 1)
            a_cor = round(df2['income'].corr(df2['squares']), 4)
            b_income = float(df_rosstat1[year_cols[1]])
            b_squares = float(df_rosstat1[year_cols[0]])
            df3 = pd.DataFrame({"region_id": [region[0]],
                                "region": [region[1]],
                                "year": [year_take],
                                "a_income": [a_income],
                                "a_squares": [a_squares],
                                "a_squares2": [a_squares2],
                                "a_cor": [a_cor],
                                "b_income": [b_income],
                                "b_squares": [b_squares]})
            df_averaged = df_averaged.append(df3)
    df_averaged.to_csv(r'data/output/averaged.csv', index=False, header=True)


def grid_map(map_type):
    df = pd.read_csv('data/declarator_rosstat/declarator_rosstat.csv')
    features_list = []
    shuffle = False
    if map_type == "square":
        features_list = ['Площадь чиновника', 'Площадь средняя']
        shuffle = True
    if map_type == "income":
        features_list = ['Доход чиновника', 'Средний доход в регионе']
        shuffle = False
    if map_type == "square2":
        features_list = ['Площадь чиновника', 'Площадь чиновника (участки)']
        shuffle = True

    plot_grid_map(df, features_list,
                  shuffle=shuffle,
                  pixels=20,
                  bar_plot=False,
                  tile_names='subj_rus',
                  fed_distr_color=True)


def h_lines():
    df = pd.read_csv('data/output/averaged.csv')
    # x = df.loc[:, ['a_cor']]
    # df['a_cor_z'] = (x - x.mean())/x.std()
    df['colors'] = ['red' if x < 0 else 'green' for x in df['a_cor']]
    df.sort_values('a_cor', inplace=True)
    df.reset_index(inplace=True)

    fig = plt.figure(figsize=(14, 28), dpi=40)
    fig.subplots_adjust(left=0.2)
    plt.hlines(y=df.index, xmin=0, xmax=df.a_cor)
    for x, y, tex in zip(df.a_cor, df.index, df.a_cor):
        t = plt.text(x, y, round(tex, 2), horizontalalignment='right' if x < 0 else 'left',
                     verticalalignment='center', fontdict={'color': 'red' if x < 0 else 'green', 'size': 14})

    plt.yticks(df.index, df.region, fontsize=12)
    plt.title(
        'Корреляция между площадью недвижимости и доходами чиновников по регионам в 2015 году',
        fontdict={'size': 20})
    plt.grid(linestyle='--', alpha=0.5)
    plt.xlim(-0.2, 1)
    plt.show()


# Initial preparations with the most common data
with open('data/description/region.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader, None)
    regions = list(reader)
years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']
with open('data/declarator_rosstat/square_income.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    rosstat = list(reader)
headers = rosstat.pop(0)
df_rosstat = pd.DataFrame(rosstat, columns=headers)


# preprocess_data_incomes()
# make_averaged_table()
# make_boxplots(years[0], dpi=80)
# make_scatterplots()
grid_map("income")
