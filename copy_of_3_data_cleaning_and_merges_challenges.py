# -*- coding: utf-8 -*-
"""Copy of 3-data-cleaning-and-merges-challenges.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16RYIjRjvU4g57stH-tVYGaQyIla8Rkfr

# Data cleaning and merging dataframes

## Loading multiple datasets

### Google way
"""

import pandas as pd

# orderlines.csv
url = 'https://drive.google.com/file/d/14Y7g5ITyf6LMyPoKc9wr010V9StaCUux/view?usp=sharing' 
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
orderlines = pd.read_csv(path)

# orders.csv
url = 'https://drive.google.com/file/d/1BLEHcP-9fm9Rv7A01H3co2XBMnSr66YC/view?usp=sharing' 
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
orders = pd.read_csv(path)

print(path)

# brands.csv
url = 'https://drive.google.com/file/d/1BrNrIY0F1LbyXtyaQygUBXVxQGB3JBqx/view?usp=sharing' 
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
brands = pd.read_csv(path)

# products.csv
url = 'https://drive.google.com/file/d/1UfsHI80cpQqGfsH2g4T4Tsw8cWayOfzC/view?usp=sharing' 
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
products = pd.read_csv(path)

df_list = [orderlines, orders, brands, products]
files = ['orderlines','orders','brands','products']

"""### Classical way

Reading file by file
"""

# import pandas as pd

# path = '../data/eniac/'
# orderlines = pd.read_csv(path + 'orderlines.csv')
# orders = pd.read_csv(path + 'orders.csv')
# brands = pd.read_csv(path + 'brands.csv')
# products = pd.read_csv(path + 'products.csv')

# df_list = [orderlines, orders, brands, products]
# files = ['orderlines','orders','brands','products']

"""### Another way

Using `os` and a loop to read all the files from a directory. It's also possible to read only files with a certain extension (like `.csv`):
"""

# import pandas as pd
# import os
# path = '../data/eniac/'
# path, dirs, files = next(os.walk(path))
# #print(files)

# # remove non-csv files
# for file in files:
#     if not file.endswith("csv"):
#         files.remove(file)

# # create empty list 
# df_list = []

# # append datasets to the list
# for file in files:
#     temp_df = pd.read_csv(path + file, sep=',')
#     df_list.append(temp_df)

# # show results
# products, orders, orderlines, brands = df_list[0], df_list[1], df_list[2], df_list[3]

"""## Data quality

### Missing values
"""

# we can check missing values column
orderlines.isna().sum()

# or for the whole dataframe
orderlines.isna().sum().sum()

orders.isna().sum()

orders.isna().sum().sum()

# the .info() method also tells us the "Non-Null Count" for each column
orderlines.info()

orders.info()

brands.info()

products.info()

products.isna().sum()

orderlines.head()

"""### Duplicates

The presence of duplicate rows is generally a sign that the data is not clean, and will deserve further exploration.
"""

orderlines.duplicated().sum()

orders.duplicated().sum()

brands.duplicated().sum()

products.duplicated().sum()

products.info()

"""### Data cleanliness - initial assessment"""



"""Based on our initial exploration, we know we will need to deal with some missing values. The biggest issue so far are the duplicates on the `products` DataFrame. Here are some aspects that we will need to fix or, at least, explore further:

* **products**: 
    * `price` and `promo_price` are loaded as objects. They should be floats. 
    * Missing values: 
        * `description`: 7 missing values. Maybe that could be inferred from the product name?
        * `price`: the missing values could be filled from the `orderlines` dataset. But first we will need to clean it. 
    * Duplicates: a total of 8746 duplicates seems to indicate this DataFrame has been seriously corrupted.
    
* **orders**: 
    * `created_date` should have a date data type. Then, it would be a good quality check to see if the created date for `orders` mathces with the created dates for `orderlines`. 
    
* **orderlines**: 
    * `unit_price` has to be a float, something is wrong there. 
    * `date` has to be transformed to a date data type. Then, as we said, check that it with matches with the `orders` dataset. 
    
* **brands**: looks fine. 

Where do we have to start? 

1. **Data consistency:** Since `orders` and `orderlines` seem very crucial to the analysis, we will start by cleaning them and checking that the information present in both DataFrames match.

2. **The "products mess":** This file seems to have many issues. We will leave it out for now and perform a proper exploration later to understand better what's going on there.

## Cleaning orders

The data consistency check we will do with `orderlines` will involve two steps: 

* the initial and last dates of the orders should be the same
* the sum of `total_paid` on both datasets should be the same

Let's start by transforming the `created_date` of the orders DataFrame and looking for its earliest and latest values:
"""

orders.info()

# change date datatype
orders['created_date'] = pd.to_datetime(orders['created_date'])

# earliest value
min(orders['created_date'])

# latest value
max(orders['created_date'])

"""Now we will look at the overall sum of `total_paid` for the orders table:"""

sum(orders['total_paid'])

"""Why do you think the result of the sum is a nan (not a number)?"""

orders["total_paid"].isna().sum()

"""There are missing values! We can explore them and see how they are all "Pending" orders:"""

orders.loc[orders['total_paid'].isna()]

"""Since these orders are only a tiny fraction and there's a valid reason why the `total_paid` value is missing, we will simply exclude them from the dataset:"""

orders.dropna(inplace=True)

"""Now the dataset is clean. And the total paid is: """

orders['total_paid'].isna().sum()

sum(orders['total_paid'])

"""## Cleaning orderlines

Following our data consistency check, will now gather in the orderlines DataFrame the same information we got from orders:

* the initial and last dates
* the sum of `total_paid`


First let's transform our date time:
"""

orderlines['date'] = pd.to_datetime(orderlines['date'])

min(orderlines['date'])
# orders: Timestamp('2017-01-01 00:07:19')

max(orderlines['date'])
# orders: Timestamp('2018-03-14 13:58:36')

"""**It's a match!**

Now let's check the `total_paid` for orderlines. It's not going to be as easy as with the orders DataFrame, considering the sturcture of orderlines:

"""

orderlines.head(3)

"""
To get this value, we will have to calculate a new column, total price for each row. It would be `product_quantity` * `unit_price`. This operation will require that both columns have a numeric data type:"""

orderlines.dtypes

"""...it's not the case right now, so we will have to transform the `unit_price` to a numeric data type. """

# uncomment the line of code below and read the error it produces:
orderlines['product_quantity']*pd.to_numeric(orderlines['unit_price'])

"""While trying to transform this column to numeric an error appears. From the error message, 

> "Unable to parse string '1.137.99' at position 6"

it seems that our dataset has some problems with the thousands separators: they were encoded as dots, and Python & pandas only admit one dot per number: the _decimal_ separator!

Lesson learned: do not use thousand separators in databases / statistical software / programming languages! Sadly, it's too late for us, and we will have to deal with the issue.

There are many ways to approach this problem. The first thing we will do is to count how many dots appear for each `unit_price` value, using string operations. If there are two or more dots a value, we will consider it corrupted ???and either try to fix it, or remove it completely.
"""

# we create a copy of the dataset
ol_temp = orderlines.copy()

# create a new column with the amount of dots in the unit_price column
ol_temp['dots'] = orderlines['unit_price'].str.count('\.') # the backslash 'escapes' the special meaning of '.' in string operations

# show the rows with more than one dot
ol_temp.query('dots > 1')

"""Our theory about the thousands separators is confirmed. How can we solve this problem? 

Let's remove all the dots for all the `unit_price`, and then add a dot before the last 2 digits to all the rows. Then we will transform it into numeric values.

##### step 1: remove all dots
a) A "corrupted" price like `1.137.99`	will become `113799`

b) A correct price like `37.99`	will become `3799`

##### step 2: add dots two digits before the end of the number
a) The "corrupted" price will go from `113799` to `1137.99`

b) The correct price will go from `3799` back to `37.99`.
"""

# step 1: to remove the dots, we replace them for... nothing
orderlines = orderlines.assign(unit_price_nd = orderlines['unit_price'].str.replace('\.','', regex=True))
orderlines.head()

# step 2.1: we first separate all numbers between the part that goes before the
# decimal point (integers) and the part that goes afterwards (deimals)
orderlines['integers'] = orderlines['unit_price_nd'].str[:-2]
orderlines['decimals'] = orderlines['unit_price_nd'].str[-2:]
orderlines.head()

# step 2.2: we now concatenate those two parts of the number, with a dot in between
orderlines['new_unit_price'] = orderlines['integers'] + '.' + orderlines['decimals']
orderlines.head()

"""We will now try again to convert this column to a numeric data type:"""

orderlines['unit_price'] = pd.to_numeric(orderlines['new_unit_price'])
orderlines.info()

"""Data cleaning done! 

Back to data consistency: Now it is time to multiply `product_quantity` and `unit price`, sum all the rows and check whether the value matches the sum of the `total_paid` from the orders DataFrame: 
"""

# drop 'auxiliary' columns
orderlines.drop(['unit_price_nd','decimals','integers','new_unit_price'], axis=1, inplace=True)

# create a new column "total_price" by multiplying product_quantity times unit_price
orderlines['total_price'] = orderlines['product_quantity'] * orderlines['unit_price']

# sum of the new column "total_price":
sum(orderlines['total_price'])

"""Sadly, it does not match exactly with the sum of `total_paid` from orders:"""

orders['total_paid'].sum()

"""The mismatch is about 383 thousand dollars, a non-neglegible amount of money:"""

sum(orderlines['total_price']) - orders['total_paid'].sum()

"""How can we figure out where does the difference come from?

## Matching `orders` and `orderlines`

It is possible that some orders exist in one dataset but not in the other one. This would be a potential source for this price mismatch. Let's find out!

We first create a new column in the `orderlines` dataset using `assign`. We also use `isin()` to create a boolen value (True/False) that checks whether the `id_order` is present in the `orders` dataset:
"""

new_df=orderlines.assign(check_orders = orderlines['id_order'].isin(orders['order_id']))
new_df.head()

orderlines["check_orders"]=orderlines['id_order'].isin(orders['order_id'])
orderlines.head()

"""Then, using `.query` we select rows where the value in this new column is `False`:"""

(
new_df
    .query("check_orders==False")
)

"""It looks like 240 rows in `orderlines` come from orders not present in the `orders` dataset. This is quite inconsistent, since the `orders` dataset should be the one and only source of truth for orders: if an order is not there, it should not exist. We will definitely report this anomaly, but for now, let's just remove those "ghost" orders:"""

orderlines = (orderlines
              .assign(check_orders = orderlines['id_order'].isin(orders['order_id']))
              .query("check_orders==True"))

"""Now let's look at this problem in the opposite direction: are there orders in the `orders` dataset not prsent in `orderlines`?"""

(orders
 .assign(check_orders = orders['order_id'].isin(orderlines['id_order']))
 .query("check_orders==False"))

"""There are more than 22000 orders in the `orders` dataset that are not present on the `orderlines` dataset!!! We can try to find out why by looking at the state of these orders:"""

(orders
 .assign(check_orders = orders['order_id'].isin(orderlines['id_order']))
 .query("check_orders==False")
 ['state'].value_counts())

"""It looks like most of them are orders that were not fully completed: the products were left in the shopping basket or the order was "placed" but maybe not paid (hence the state "Place Order". Some of them were "Completed", though. 

This will require further research, and we might have to come back to these orders if we have to explore consumer behaviour (e.g. why are orders left in the shopping basket?), but for now, for the sake of data consistency, let's drop all of these unmatched orders:
"""

orders = (orders
          .assign(check_orders = orders['order_id'].isin(orderlines['id_order']))
          .query("check_orders==True")
         )

"""Let's now check again if the total paid matches:"""

orders['total_paid'].sum()

orderlines['total_price'].sum()

"""STILL NOT MATCHING!!! And actually, the difference got larger. This is outrageous. Let's keep exploring."""

orderlines['total_price'].sum() - orders['total_paid'].sum()

"""## Solving the price mismatch

Let's merge both datasets and compare, order by order, the `total_price`. We will call this new merged dataset `orders_info`.

*Note: Remember that the `orderlines` dataset contains one row per product bought: an order where 3 different products were purchased will result in 3 rows there. Therefore, to merge `orderlines` with `orders`, we have to group `orderlines` by its `id_order` and aggregate it by taking the sum of the `total_price`.
"""



orderlines_agg = orderlines\
    .groupby('id_order')\
    .agg({'total_price':'sum'})

orders_info = (
    orderlines_agg.merge(orders, how='left', left_on='id_order', right_on='order_id')
    .copy()
)
orders_info

orders_info = (
orderlines
    .groupby('id_order')
    .agg({'total_price':'sum'})
    .merge(orders, how='left', left_on='id_order', right_on='order_id')
    .copy()
)
orders_info

orderlines.rename(columns={'id_order':'order_id'}, 
                   inplace=True)
orderlines

#merged_orders = pd.merge(orderlines, orders, on='order_id', how='outer')
#merged_orders
#merged_orders.head(30)

"""Now that the `total` from both datasets is in the same dataframe, we can create a new column with the difference:"""

orders_info['price_difference'] = orders_info['total_price'] - orders_info['total_paid']
orders_info.sort_values('price_difference').tail(30)

orders_info['price_difference'].describe()

"""Looks like the maximum and minimun price differences are huge: some orders are really corrupted. But we also see from the mean and the quartiles that the price difference is neglegible for most orders.

## Challenge: Remove outliers

Decide on a criteria for removing orders whenever you cannot trust the price difference between `orders` and `orderlines`. 

Note: this solution does not completely achieve 100% trustable data, but the objective here is to end up with the best possible data with a limited amount of time, which makes a complete revision of the database protocols and the data pipelines is not feasable - and business questions are pending. Documenting and reporting this data cleaning process, including the criteria that you will use for determining what do you consider an "outlier", is key. Not being paralized by it is also important!
"""

# you code here
#import pandas as pd

def remove_outliers(df,columns,n_std):
    for col in columns:
        print('Working on column: {}'.format(col))
        
        mean = df[col].mean()
        sd = df[col].std()
        
        df = df[(df[col] <= mean+(n_std*sd))]

"""Save the data once you are sure you can trust it!"""

# run the code only once your "orderlines" and "orders" are clean
#orderlines.to_csv('orderlines_clean.csv', index=False)
#orders.to_csv('orders_clean.csv', index=False)

#from google.colab import files
#files.download("orderlines_clean.csv")
#files.download("orders_clean.csv")

"""## Challenge: Cleaning products

Now it is time to clean the products dataset. Let's do a quick review of its major problems:
"""

print(products.info(), "\n")
print("Missing values:", products.isna().sum(), "\n")
print("Duplicate rows:", products.duplicated().sum())

"""Looking at this overview, we can see that there are different things that have to be changed: 

* Data types: 
    * `price` should be a float
    * `promo price` should be a float
* Duplicated rows. They have to be removed. 
    * To accomplish this step you can use the method `pd.DataFrame.drop_duplicates()`. Be sure you drop all the duplicates based on the column **sku**, as it is the one you will use to merge with orderlines. 
* Missing values: 
    * Description maybe can be inferred by the name
    * `price`. Is there a way we can extract the information from another table?
    * `type`. Do we need this column for our analysis?
    
This task can be accomoplished by using all the methods you already know.

### Start of the challenge

#### Duplicates
"""

# code here
#pd.products.drop_duplicates()

#pd.products.drop_duplicates(subsets=['sku'])
#products.drop_duplicates(subset=['sku'])

#using subset option 
df3 = products.drop_duplicates(subset=['sku'])
print(df3)

products.duplicated().sum()

"""#### Fix data types"""

# code here
products['promo_price']to_numeric(products['unit_price'])
#orderlines['product_quantity']*pd.to_numeric(orderlines['unit_price'])

products['price']= pd.to_numeric['price']
#products_unique["price_nd"]= pd.to_numeric(products_unique["price_nd"])
#print(df.dtypes)

"""##### Deal with the "price" column"""

# code here

"""#### Missing values"""

#checking missing values for  desc
desc_missing = pd.isnull(products["desc"])
products[desc_missing]

#filling missing values with 'no description'
products["desc"].fillna("No description", inplace = True)
products.info()
print("Missing values:", products.isna().sum(), "\n")

"""#### Save & Download the clean products dataset"""

products['desc']

#creating copy of altered product notebook
products_unique = products.copy()

# create a new column with the amount of dots in the unit_price column
products_unique['dot_3'] = products['promo_price'].str.count('\.') # the backslash 'escapes' the special meaning of '.' in string operations

# show the rows with more than one dot
products_unique.query('dots > 0')

#silvia's code

products_unique["dot_3"] = products_unique["price"].str.count(".\d{2}")

products_unique.loc[products_unique['dot_3']>0]
products_unique.groupby("dot_3").describe()

products_unique = products_unique.assign(price_nd = products_unique['price'].str.replace('.','', regex=True))
products_unique["price_nd"]= pd.to_numeric(products_unique["price_nd"])

import numpy as np
condlist = [products_unique.dot_3==0, products_unique.dot_3==1, products_unique.dot_3==2 ]

choicelist = [products_unique["price_nd"],products_unique["price_nd"]0.01,products_unique["price_nd"]0.001]
products_unique["price_c"]=np.select(condlist, choicelist)
products_unique.head(15)
products_unique.tail(15) # Strange things are happening in this data set!

"""## Brands

The brands csv looks fine, so we can work together with it.
"""

#brands.to_csv('brands_clean.csv', index=False)
#files.download("brands_clean.csv")