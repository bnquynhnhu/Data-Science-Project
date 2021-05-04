# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 23:42:13 2021

@author: Nhu Nguyen
"""

global token
from AirDNA import getToken, getUpdatedTokenIfLoggedInUser, returnCityID, returnListings
import logging
import config as cfg

if __name__ == "__main__":
    logfile = cfg.basedir + '\\airdna.log'
    logging.basicConfig(filename=logfile,level=logging.INFO)

    # First, we get the returned user token when user logins successfully
    token = getToken()
    
    # After we login successfully, an returned update user token will be issued
    updatedToken = getUpdatedTokenIfLoggedInUser()
    
    # Get the city ID
    # country='fr'; city='toulouse'; state='occitania'
    country='fr'; state='ile-de-france'; city='paris'; 

    cityID = returnCityID(updatedToken, country, city, state)
    print(cityID)
    
    # Find the list of properties of the selected city
    num_listing = returnListings(updatedToken, cityID)