import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import missingno as msno
from datetime import date
import researchpy as rp
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
#pd.set_option('display.float_format', lambda x: '%.4f' % x)

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

df=pd.read_csv('/Users/serhandulger/armut_data.csv')

df.head()

def check_df(dataframe, head=3):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### NA SUM #####################")
    print(dataframe.isnull().sum().sum())
    print("##################### Describe #####################")
    print(dataframe.describe())
    print("##################### Nunique #####################")
    print(dataframe.nunique())

check_df(df)

import datetime as dt
df["CreateDate"] = pd.to_datetime(df["CreateDate"]).dt.normalize()

# Creating NEW Variables

df["Service"] = df["ServiceId"].astype(str) + '_' + df["CategoryId"].astype(str)
df["Basket"] = df["UserId"].astype(str) + '_' + df["CreateDate"].astype(str).str[:7]

df.head()

basket = (df.groupby(["Basket", "Service"])["ServiceId"]
              .count().unstack().fillna(0)
              .applymap(lambda x: 1 if x > 0 else 0))

basket.head()

frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)

frequent_itemsets.sort_values(by='support',ascending=False).head(10)

rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)

sorted_rules = rules.sort_values("lift", ascending=False)

sorted_rules.head()


def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []

    for i, product in sorted_rules["antecedents"].items():
        for j in list(product):  # antecedent i yani urunu secti
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"]))

    recommendation_list = list({item for item_list in recommendation_list for item in item_list})

    return recommendation_list[:rec_count]

arl_recommender(rules, "2_0", 3)

arl_recommender(rules, "2_0", 4)