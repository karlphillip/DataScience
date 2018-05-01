import math
import pandas as pd
import numpy as np
import time

# try to import TQDM module to display progress bar
with_tqdm = True
try:
    from tqdm import tqdm_notebook as tqdm
    pbar = tqdm(total = 9)
except ImportError:
    with_tqdm = False    

    
# def testme():    
#     if (with_tqdm): 
#         for i in range(11+1):
#             pbar.update(i - pbar.n)
#             time.sleep(1)
#         pbar.close()
    
    
def load_from(pwd):
    if (with_tqdm): 
        pbar.update(1)
        
    ###
    ### 1. Load Datasets
    ###
    air_reserve_df = pd.read_csv(pwd + '/air_reserve.csv')
    air_store_df = pd.read_csv(pwd + '/air_store_info.csv')
    air_visit_df = pd.read_csv(pwd + '/air_visit_data.csv')

    hpg_reserve_df = pd.read_csv(pwd + '/hpg_reserve.csv')
    hpg_store_df = pd.read_csv(pwd + '/hpg_store_info.csv')

    date_info_df = pd.read_csv(pwd + '/date_info.csv')
    store_ids_df = pd.read_csv(pwd + '/store_id_relation.csv')
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.1  air_df = air_visit_df + air_reserve_df
    ###

    # Add a visit_date column for air_reserve
    air_reserve_df['visit_datetime'] = pd.to_datetime(air_reserve_df['visit_datetime'])
    air_reserve_df['visit_date'] = air_reserve_df['visit_datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))

    reserve = air_reserve_df[["air_store_id","visit_date","reserve_visitors"]].groupby(["air_store_id","visit_date"], as_index = False).sum()
    reserve.rename(columns = {'reserve_visitors': 'reservations'}, inplace = True)
    air_df = pd.merge(air_visit_df, reserve, on = ['visit_date','air_store_id'], how = "left")
      
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.2  air_df = air_df + air_store_df
    ###

    air_df = pd.merge(air_df, air_store_df, on="air_store_id", how="inner")
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.3  hpg_df = hpg_reserve_df + hpg_store_df
    ###

    hpg_df = pd.merge(hpg_reserve_df, hpg_store_df, on="hpg_store_id", how="inner")

    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.4 hpg_df = hpg_df + store_ids_df
    ###

    # convert visit_datetime from string to datetime object to add a new column containing only the Y-M-D
    hpg_df['visit_datetime'] = pd.to_datetime(hpg_df['visit_datetime'])
    hpg_df['visit_date'] = hpg_df['visit_datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))

    hpg_df = pd.merge(hpg_df, store_ids_df, on='hpg_store_id', how='inner')
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.5 df = air_df + hpg_df
    ###

    # rename columns in both dataframes so they blend in nicely during merge
    hpg_df.rename(columns={'reserve_visitors': 'reservations'}, inplace=True)
    hpg_df.rename(columns={'hpg_genre_name': 'genre_name'}, inplace=True)
    hpg_df.rename(columns={'hpg_area_name' : 'area_name'}, inplace=True)
    hpg_df.drop('hpg_store_id',  axis=1, inplace=True)

    air_df.rename(columns={'air_genre_name': 'genre_name'}, inplace=True)
    air_df.rename(columns={'air_area_name' : 'area_name'}, inplace=True)

    hpg_cols = ['air_store_id', 'visit_date', 'reservations']
    df = pd.merge(air_df, hpg_df[hpg_cols], on=hpg_cols[:-1], how='left')

    df['reservations'] = df['reservations_x'] + df['reservations_y']
    df.drop(['reservations_x', 'reservations_y'], 1, inplace=True)
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.6 df = df + date_info_df
    ###

    # combine both datasets to add columns 'day_of_week' and 'holiday_flg' to df
    df = pd.merge(df, date_info_df, left_on='visit_date', right_on='calendar_date', how='left')
    del df['calendar_date']
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 4. Cleaning Data
    ###

    # TODO handle NaN on reservations
    
    if (with_tqdm): 
        pbar.update(1) 
        pbar.close()

    return df
    