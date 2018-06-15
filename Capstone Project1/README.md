## Project Proposal: Recruit Restaurant Visitor Forecasting

Problem
-------
Weather and local competition are unpredictable factors that make it harder for Recruit Holdings’ restaurants to effectively predict how many customers they should expect at any given day. Knowing this in advance would allow them to make better preparations, purchase all the necessary ingredients and schedule staff members. The purpose of this Kaggle competition is to use reservation, visitation and other data to predict the number of visitors a restaurant is going to have in a future date.

Who might care?
---------------
The ability to predict how many customers a restaurant should expect at any given day is something interesting to every restaurant on the planet. Being able to purchase the proper amount of ingredients instead of seeing them slowly expire on the shelf saves restaurants valuable resources. By becoming smarter consumers, restaurants are also helping the planet use less resources. Besides, restaurants and businesses alike, data scientists and machine learning scientists also have a reason to care: Kaggle placed a $25.000 reward for the best solution for this problem.

Data
----
The [competition page](https://www.kaggle.com/c/recruit-restaurant-visitor-forecasting) provides reservation and visition data which are relational datasets from two systems. Each file is prefaced with the source (either *air_* or *hpg_*) to indicate its origin:
  - The first, means that the data came from to AirREGI/Restaurant Board(air), similar to Square, a reservation control and cash register system.
  - The second is a reference Hot Pepper Gourmet, similar to Yelp, a site where users can search restaurants and make reservations online.

Each restaurant has a unique *air_store_id* and *hpg_store_id*. Not all restaurants are covered by both systems. 

These are the files available for download:
  - **air_reserve.csv (5.8MB)**: reservations made in the air system (air_store_id, visit_datetime, reserve_datetime, reserve_visitors);
  - **hpg_reserve.csv (126MB)**: reservations made in the hpg system (hpg_store_id, visit_datetime, reserve_datetime, reserve_visitors);
  - **air_store_info.csv (74KB)**: contains information about select air restaurants (air_store_id, air_genre_name, air_area_name, latitude, longitude).
  - **hpg_store_info.csv (478KB)**: contains information about select hpg restaurants (hpg_store_id, hpg_genre_name, hpg_area_name, latitude, longitude
  - **store_id_relation.csv (6KB)**: this file allows you to link restaurants that have both the air and hpg systems (air_store_id, hpg_store_id).
  - **air_visit_data.csv (8.7MB)**: historical visit data for the air restaurants (air_store_id, visit_date, visitors).
  - **date_info.csv (10KB)**: basic information about the calendar dates in the dataset (calendar_date, day_of_week, holiday_flag).

Modeling Approach
-----------------
To be able to predict how many visitors a restaurant will receive in a future date, exploratory data analysis will be initially performed on the data to clean and merge the files. This allows a better visualization of the time series data. Finally, different regression techniques are going to be tested to predict the number of visitors more accurately.

Deliverables
------------
The following items are going to be shared at the end of the project:
  - The source code of the application;
  - The original datasets;
  - Jupyter notebooks, showing in great detail the approach used for modeling;  
  - The final project report;
  - The final project presentation (slide decks);
