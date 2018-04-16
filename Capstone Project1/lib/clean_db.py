import math
import pandas as pd
import numpy as np
import time

# try to import TQDM module to display progress bar
with_tqdm = True
try:
    from tqdm import tqdm_notebook as tqdm
    pbar = tqdm(total = 12)
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
    ### 3.1  df = air_visit_df + air_reserve_df
    ###

    # Add a visit_date column for air_reserve
    air_reserve_df['visit_datetime'] = pd.to_datetime(air_reserve_df['visit_datetime'])
    air_reserve_df['visit_date'] = air_reserve_df['visit_datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))

    # Rename columns so they match during merge
    air_reserve_df.rename(columns={'reserve_visitors': 'visitors'}, inplace=True)
    df = pd.merge(air_visit_df, air_reserve_df, on=["air_store_id", "visit_date", "visitors"], how="outer")
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.2  df = df + air_store_df
    ###

    df = pd.merge(df, air_store_df, on="air_store_id", how="left")
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.3  hpg_df = hpg_reserve_df + store_ids_df
    ###

    # convert visit_datetime from string to datetime object to add a new column containing only the Y-M-D
    hpg_reserve_df['visit_datetime'] = pd.to_datetime(hpg_reserve_df['visit_datetime'])
    hpg_reserve_df['visit_date'] = hpg_reserve_df['visit_datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))

    # replace the HPG code in hpg_merged_df for its equivalent AIR code
    hpg_df = pd.merge(hpg_reserve_df, store_ids_df, on='hpg_store_id', how='left')
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.4 hpg_df = hpg_df + hpg_store_df
    ###

    hpg_df = pd.merge(hpg_df, hpg_store_df, on="hpg_store_id", how="left")
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.5 df = df + hpg_df
    ###

    # rename columns in both dataframes so they blend in nicely during merge
    hpg_df.rename(columns={'reserve_visitors': 'visitors'}, inplace=True)
    hpg_df.rename(columns={'hpg_genre_name': 'genre_name'}, inplace=True)
    hpg_df.rename(columns={'hpg_area_name' : 'area_name'}, inplace=True)
    df.rename(columns={'air_genre_name': 'genre_name'}, inplace=True)
    df.rename(columns={'air_area_name' : 'area_name'}, inplace=True)

    df = pd.concat([df, hpg_df], axis=0).reset_index(drop=True)
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 3.6 df = df + date_info_df
    ###

    # convert column visit_datetime from string to datetime object
    df['visit_datetime'] = pd.to_datetime(df['visit_datetime'])

    # combine both datasets to add columns 'day_of_week' and 'holiday_flg' to merged_df
    df = pd.merge(df, date_info_df, left_on='visit_date', right_on='calendar_date')
    del df['calendar_date']
    
    if (with_tqdm): 
        pbar.update(1) 

    ###
    ### 4. Cleaning Data
    ###

    # 4.7.1 NaN on string columns
    df['area_name'].fillna(value='', inplace=True)
    df['genre_name'].fillna(value='', inplace=True)
    
    if (with_tqdm): 
        pbar.update(1) 

    # 4.7.2 NaN on float columns air_store_id and hpg_store_id
    df.fillna(pd.concat([ df.hpg_store_id.map(store_ids_df.set_index('hpg_store_id').air_store_id),
                          df.air_store_id.map(store_ids_df.set_index('air_store_id').hpg_store_id),
                        ], axis=1, keys=['air_store_id', 'hpg_store_id']), inplace=True)

    df['air_store_id'].fillna(value='', inplace=True)
    df['hpg_store_id'].fillna(value='', inplace=True)
    
    if (with_tqdm): 
        pbar.update(1) 

    # 4.7.3 NaN on numeric columns
    df['latitude'].fillna(value=-1, inplace=True)
    df['longitude'].fillna(value=-1, inplace=True)
    
    if (with_tqdm): 
        pbar.update(1) 

    # 4.7.4 NaN on datetime columns
    df['reserve_datetime'].fillna(value=-9999, inplace=True)
    df['visit_datetime'].fillna(value=-9999, inplace=True)
    
    if (with_tqdm): 
        pbar.update(1) 
        pbar.close()

    return df
    