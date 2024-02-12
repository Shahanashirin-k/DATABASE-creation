# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 20:37:13 2023

@author: SHAHANA SHIRIN
"""
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import sqlite3

#Initialise faker as fake for creatig fake data 
fake = Faker()

# Create SQLite connection and cursor
conn = sqlite3.connect('restaurant_database.db')
# Enable Foreign Keys
conn.execute("PRAGMA foreign_keys = on;")  
cursor = conn.cursor()

# Create Restaurants table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Restaurants (
        RestaurantID INTEGER PRIMARY KEY,
        RestaurantName TEXT NOT NULL,
        Cuisine TEXT NOT NULL,
        PriceRange TEXT NOT NULL,
        Address TEXT NOT  NULL,
        PhoneNumber TEXT NOT NULL,
        Website TEXT NOT NULL
    )
''')

# Create Customers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        EmailAddress TEXT NOT NULL,
        Address TEXT NOT NULL,
        PhoneNumber TEXT NOT NULL,
        RestaurantID INTEGER NOT NULL,
        ReviewRating TEXT NOT NULL,
        FOREIGN KEY (RestaurantID) REFERENCES Restaurants (RestaurantID)
    )
''')

# Create Orders table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID INTEGER PRIMARY KEY,
        CustomerID INTEGER NOT NULL,
        OrderDate DATETIME NOT NULL,
        OrderAmount REAL NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID)
    )
''')

# Create Dishes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dishes (
        DishID INTEGER PRIMARY KEY,
        DishName TEXT NOT NULL,
        Cuisine TEXT NOT NULL,
        Price REAL NOT NULL
    )
''')

# Commit changes to save the table structure
conn.commit()

# Set seed for reproducibility
np.random.seed(100)

# Set the number of rows in the dataset
n_restaurant=1000

# Generate random data for Restaurant Table
restaurant_ids = range(1,n_restaurant+1 )  #nominal data
restaurant_names = [fake.company() for _ in range(n_restaurant)]  #nominal data
cuisines = ['Italian', 'Mexican', 'Chinese', 'Indian', 'American'] #ordinal data
price_ranges = np.random.uniform(5.0, 100.0, n_restaurant) #ratio data
addresses = [fake.address() for _ in range(n_restaurant)] #nominal data
phone_numbers = [fake.numerify('07##-#######')  for _ in range(n_restaurant)] #nominal data
websites = ['https://www.' + fake.company().lower() + '.com' for _ in range(n_restaurant)] #nominal data

# Create DataFrame for restuarent data
restaurant_data = pd.DataFrame({
    'RestaurantID': restaurant_ids,
    'RestaurantName': restaurant_names,
    'Cuisine': np.random.choice(cuisines,n_restaurant),
    'PriceRange': price_ranges,
    'Address': addresses,
    'PhoneNumber': phone_numbers,
    'Website': websites
})

# Generate random data for customer table
customer_ids = range(1, n_restaurant+1)   # Nominal data
first_names = [fake.first_name() for _ in range(n_restaurant)]   # Nominal data
last_names = [fake.last_name() for _ in range(n_restaurant)]   # Nominal data
email_addresses = [fake.email() for _ in range(n_restaurant)]   # Nominal data
addresses = [fake.address() for _ in range(n_restaurant)]  # Nominal data
ratings = ['Poor', 'Average', 'Good', 'Excellent']  # ordinal data
review_ratings = np.random.choice(ratings, 1000, p=[0.1, 0.2, 0.4, 0.3])                                   

# Create DataFrame for custemer
customer_data = pd.DataFrame({
    'CustomerID': customer_ids,
    'FirstName': first_names,
    'LastName': last_names,
    'EmailAddress': email_addresses,
    'Address': addresses,
    'PhoneNumber': phone_numbers,
    'RestaurantID': restaurant_ids,
    'ReviewRating': review_ratings,
})

# Generate random data for order table
menu_categories = ['Appetizer', 'Main Course', 'Dessert','Light Food']  
menu_items = {
    'Appetizer': ['Salad', 'Spring Rolls', 'Bruschetta'],
    'Main Course': ['Pasta', 'Grilled Chicken', 'Steak'],
    'Dessert': ['Chocolate Cake', 'Ice Cream', 'Fruit Tart'],
    'Light Food': ['Vegetable Wrap', 'Quinoa Salad', 'Fruit Smoothie']
    }
menu_category_data = np.random.choice(menu_categories, n_restaurant)  # Nominal data
menu_item_data = [np.random.choice(menu_items[category]) for category in menu_category_data]  # Nominal data
quantities_data = np.random.randint(1, 5, n_restaurant)  #ordinal data 
customer_rating_data = np.random.choice(ratings, n_restaurant, p=[0.1, 0.2, 0.4, 0.3])  # Ordinal data
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 1)
order_timestamps = [start_date + timedelta(minutes=np.random.randint(1, 1440)) for _ in range(n_restaurant)]  #Interval data
order_amount = price_ranges*quantities_data  #Ratio data:

# Create DataFrame for orders
order_data = pd.DataFrame({
    'OrderID': range(1, n_restaurant + 1),
    'Quantity': quantities_data,
    'MenuItemID': range(1,n_restaurant + 1),
    'MenuCategory': menu_category_data,
    'MenuItem': menu_item_data,
    'CustomerID': customer_ids,
    'RestaurantID': restaurant_ids,
    'CustomerRating': customer_rating_data,
    'OrderTimestamp': order_timestamps,
    'OrderAmount': order_amount
})

# Generate random data for dishes tablee
dish_data = pd.DataFrame({
    'DishID': range(1, n_restaurant + 1),  #nominal data
    'DishName':menu_item_data ,  #nominal data
    'Cuisine': np.random.choice(cuisines,n_restaurant),  #ordinal data
    'Price': price_ranges  #ratio data
})

# Print the restaurant data
print("Restaurant Table:")
print(restaurant_data)
# Print the customer Table
print("\nCustomer Table:")
print(customer_data)
# Print the order Table
print("\nOrder Table:")
print(order_data)
#print the dishes Table
print("\nDishes Table:")
print(dish_data)

# Insert data into tables, save this data in sqlite database
restaurant_data.to_sql('Restaurants', conn, index=False, if_exists='replace')
customer_data.to_sql('Customers', conn, index=False, if_exists='replace')
dish_data.to_sql('Dishes', conn, index=False, if_exists='replace')
order_data.to_sql('Orders', conn, index=False, if_exists='replace')

# Commit changes and close the connection
cursor.close()
conn.commit()
conn.close()





