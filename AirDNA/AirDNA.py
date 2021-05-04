# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 22:51:24 2021

@author: Nhu Nguyen
"""

import requests
import os
import pandas as pd
import logging
import config as cfg


def get_csv(filename):
    path = os.path.dirname(__file__)
    filepath = f"{path}\ETL\data\{filename}.xlsx"
    return filepath

def save_to_csv(df):
    csv_path = cfg.basedir + '\\ETL\\data\\airbnb.xlsx'
    print(csv_path)
    df.to_csv(csv_path, index=False)
    
# get the token when user log-in
def getToken():
    # Log in and get Token
    logging.info('Pushing data to %s in getToken() function' %(cfg.pushLoginURL))
    
    try:
        response = requests.post(cfg.pushLoginURL, data=cfg.myLoginData)
    except requests.RequestException as e:
        logging.error(str(e))
        
    if (response.status_code == 200):
        token = response.json()
        token = token['token']
        logging.info('Returned token: %s' %(token))
        return token
    # error
    else:
        logging.error(response.text)

        try:
            r_json = response.json()
        except ValueError:
            r_json = {}            
            msg = r_json.get('error', {}).get('message', 'Failed to get error details.')
            logging.error(msg)
            
# get the updated token of the logged in user
def getUpdatedTokenIfLoggedInUser():
    # Log in and get Token
    logging.info('Pushing data to %s in getUpdatedTokenIfLoggedInUser() function' %(cfg.pushLoggedinURL))
    
    try:
        response = requests.post(cfg.pushLoggedinURL, data=cfg.myLoggedInData)
    except requests.RequestException as e:
        logging.error(str(e))

    if (response.status_code == 200):
        token = response.json()
        token = token['token']
        logging.info('Returned updated token: %s' %(token))
        return token
    # error
    else:
        logging.error(response.text)

        try:
            r_json = response.json()
        except ValueError:
            r_json = {}            
            msg = r_json.get('error', {}).get('message', 'Failed to get error details.')
            logging.error(msg)

def returnCityID(token, country, city, state):
    url = cfg.areaLookupURL + f"access_token={token}&country={country}&city={city}&state={state}"
    logging.info('Request data from %s in returnCityID() function' %(url))

    headers = {
      'cache-control': 'no-cache'
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except requests.RequestException as e:
        logging.error(str(e))
    
    if (response.status_code == 200):
        r_json = response.json()
        city_id = r_json['area_info']['city']['id']
        
        logging.info(f"Token: {token}")
        logging.info(f"Country: {country}")
        logging.info(f"City: {city}")
        logging.info(f"State: {state}")
        logging.info(f"City ID: {city_id}")
        
        return city_id
    else:
        logging.error(response.text)

        try:
            r_json = response.json()
        except ValueError:
            r_json = {}            
            msg = r_json.get('error', {}).get('message', 'Failed to get error details.')
            logging.error(msg)               
            
def returnListings(token, city_id):
    # Get listing and ID Airbnb of a city
    url_property_list = cfg.propertyList + f"access_token={token}&city_id={city_id}&start_month=1&start_year=2017&number_of_months=36&show_regions=true"
    logging.info('Request data from %s in returnListings() function' %(url_property_list))
    
    try:
        response = requests.request("GET",url_property_list)
    except requests.RequestException as e:
        logging.error(str(e))
    
    if (response.status_code == 200):
        val_json = response.json()
        
        # get the number of listings
        num_listing = val_json['listings_returned'] 
        data_properties = val_json['properties'] 
        
        df_properties = pd.DataFrame(data_properties)
        df_properties = df_properties[["airbnb_property_id", "bedrooms", "reviews", "longitude", "latitude", "room_type"]]
        
        print(df_properties.head())
        save_to_csv(df_properties)
            
        logging.info(f"There is {num_listing} properties in the city {city_id}")
        #logging.info(f"List of properties: {lst_properties}")
            
        return num_listing#, lst_properties
    else:
        logging.error(response.text)

        try:
            r_json = response.json()
        except ValueError:
            r_json = {}            
            msg = r_json.get('error', {}).get('message', 'Failed to get error details.')
            logging.error(msg)
