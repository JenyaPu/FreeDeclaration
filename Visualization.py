import sqlite3
import pandas as pd
import seaborn as sns
# import numpy as np
# import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings(action='once')


def preprocess_data_incomes():
    conn1 = sqlite3.connect("data/database/incomes.db")
    df_income = pd.read_sql_query("SELECT * FROM incomes", conn1)
    conn1.close()

    new_df = pd.DataFrame(columns=['region', 'incomes'])
    for index, row in df_income.iterrows():
        region = row['region']
        all_incomes = row['incomes_2017']
        all_incomes = all_incomes.split(" ")
        for income in all_incomes:
            if income != "":
                if 0 < float(income) < 100000000:
                    new_df = new_df.append({'region': region, 'incomes': float(income)}, ignore_index=True)
                else:
                    print(income)
    print(new_df)

    conn2 = sqlite3.connect('data/database/incomes_processed.db')
    new_df.to_sql(name='incomes', con=conn2)
    conn2.close()


def make_boxplot(df):
    # Draw Plot
    plt.figure(figsize=(50, 10), dpi=50)
    sns.boxplot(x='region', y='incomes', data=df, notch=False)

    # Add N Obs inside boxplot (optional)
    def add_n_obs(df1, group_col, y):
        medians_dict = {grp[0]: grp[1][y].median() for grp in df1.groupby(group_col)}
        xticklabels = [x.get_text() for x in plt.gca().get_xticklabels()]
        n_obs = df1.groupby(group_col)[y].size().values
        for (x, xticklabel), n_ob in zip(enumerate(xticklabels), n_obs):
            plt.text(x, medians_dict[xticklabel]*1.01, "N: "+str(n_ob),
                     horizontalalignment='center', fontdict={'size': 14}, color='white')

    add_n_obs(df, group_col='region', y='incomes')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=75)

    # Decoration
    plt.title('Доход чиновников в различных регионах России', fontsize=22)
    # plt.ylim(10, 40)
    plt.show()


# preprocess_data_incomes()
conn = sqlite3.connect("data/database/incomes_processed.db")
df_incomes = pd.read_sql_query("SELECT * FROM incomes", conn)
conn.close()
make_boxplot(df_incomes)
