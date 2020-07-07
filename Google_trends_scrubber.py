# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:44:08 2020

@author: Trevor Gratz 

Use:
    This file is intended to be run routinely in order to scrub Google Tends
    geoMap CSV data. Users will need to alter the list_of_searchs to reflect
    their needs. Currently, the scrubber expects the downloaded data to be in
    a user's profile download folder (for Windows). If this is not the case the
    downloadfolder variable will need to be changed. Users may want to alter 
    the pre_process function to fit their needs. 
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import os
import time
import shutil
from datetime import date
import pandas as pd

# Set up pathways
dirfold = os.path.dirname(os.path.abspath(__file__))
move_data_to = os.path.join(dirfold, 'Data')
downloadfolder = os.path.join(os.environ['USERPROFILE'], 'Downloads')
driver_path = os.path.join(dirfold, 'chromedriver.exe')


def google_trend(search_term, time_period='past_day', region='both',
                 download_folder='Not provided', 
                 folder_dest='Not provided'):
    
    '''
        Parameters
    ----------
    search_term : String
        A string of the search term you wish to enter into Google Trends.
    region : String, optional
        DESCRIPTION. Decide to download data at the region levels of state,
        DMA-level, or both. Options are 'state', 'dma', and 'both'.
        The default is 'both'.
    time_period : String, optional
        DESCRIPTION. Time-period to gather data on the search term for.
        Options are 'past_day', 'past_7_days', 'past_30_days', 'past_90_days'
        and 'past_12_months'. The default is 'past_day'.
    download_folder: String
        The pathway to the downloaded data
    folder_dest: String
        The pathway to the folder to move the downloaded data to.

    Returns
    -------
    None.

    '''

    # Set up driver
    driver = webdriver.Chrome(executable_path=driver_path)
    wait = WebDriverWait(driver, 15)
    driver.get('https://trends.google.com/trends/?geo=US')
    driver.set_window_size(1535, 720)

    # Enter Search Term
    search_bar = wait.until(EC.presence_of_element_located((By.ID,
                                                            'input-254')))
    search_bar.clear()
    search_bar.send_keys(search_term + '\n')  # \n is like hitting enter

    # Click drop down time menu
    header = wait.until(EC.presence_of_element_located((By.ID, 'header')))
    action_click_time = webdriver.common.action_chains.ActionChains(driver)
    action_click_time.move_to_element_with_offset(header, 430, 225)
    action_click_time.click()
    action_click_time.perform()

    # Click user-chosen time period
    time_period_dic = {'past_day': (400, 260),
                       'past_7_days': (400, 280),
                       'past_30_days': (400,340),
                       'past_90_days': (400, 380),
                       'past_12_months': (400, 120)}

    action_choose_time = webdriver.common.action_chains.ActionChains(driver)
    action_choose_time.move_to_element_with_offset(header,
                                                   time_period_dic[time_period][0],
                                                   time_period_dic[time_period][1])
    action_choose_time.click()
    action_choose_time.perform()

    # Find anchor on middle of page
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 500)")
    geomap_anchor = wait.until(EC.presence_of_element_located((By.ID,
                                                               'GEO_MAP')))

    # Download State data
    if region == 'both' or region == 'state':
        action_download_subregion = webdriver.common.action_chains.ActionChains(driver)
        action_download_subregion.move_to_element_with_offset(geomap_anchor,
                                                              1060, 100)
        action_download_subregion.click()
        action_download_subregion.perform()
        time.sleep(2)

        # Rename files
        if download_folder != 'Not provided' and folder_dest != 'Not provided':
            download_to = os.path.join(folder_dest,
                                       f'googletrends_{search_term}_state.csv')
            downloaded_in = os.path.join(download_folder, 'geoMap.csv')
            shutil.move(downloaded_in, download_to)

    # Download DMA data
    if region == 'dma' or region == 'both':
        click_region_dropdown = webdriver.common.action_chains.ActionChains(driver)
        click_region_dropdown.move_to_element_with_offset(geomap_anchor,
                                                          1000, 100)
        click_region_dropdown.click()
        click_region_dropdown.perform()

        time.sleep(1)
        click_metro = webdriver.common.action_chains.ActionChains(driver)
        click_metro.move_to_element_with_offset(geomap_anchor, 1000, 150)
        click_metro.click()
        click_metro.perform()

        time.sleep(1)
        download_metro = webdriver.common.action_chains.ActionChains(driver)
        download_metro.move_to_element_with_offset(geomap_anchor, 1060, 100)
        download_metro.click()
        download_metro.perform()
        time.sleep(2)

        if download_folder != 'Not provided' and folder_dest != 'Not provided':
            download_to = os.path.join(folder_dest,
                                       f'googletrends_{search_term}_dma.csv')
            downloaded_in = os.path.join(download_folder, 'geoMap.csv')
            shutil.move(downloaded_in, download_to)
   
    driver.quit()


def pre_process(search_term, folder = move_data_to):
    
    
    '''
    Preprocesses the data for importation into a SQL database. Users need may
    differ and this function should be altered to reflect that

    Parameters
    ----------
    Search_term : STRING
        The search string.

    folder : STRING
        Where the data sits.
        The default is move_data_to.

    Returns
    -------
    None.

    '''
    for i in ['dma', 'state']:
        fname = os.path.join(move_data_to,
                             f'googletrends_{search_term}_{i}.csv')
        prep_file = pd.read_csv(fname, skiprows=3, header=None)
        prep_file['term'] = search_term
        prep_file['search_date'] = date.today()
        if i == 'dma':
            prep_file.rename(columns={0: 'dma', 1: 'interest'}, inplace=True)
            prep_file = prep_file[['term', 'dma', 'search_date', 'interest']]

        else:
            prep_file.rename(columns={0: 'state_val', 1: 'interest'}, inplace=True)
            prep_file = prep_file[['term', 'state_val', 'search_date', 'interest']]

        prep_file.to_csv(fname, index=False)

##############################################################################
# Example of  how to use the functions above.
# Note that currently the pre-process functions expects both the dma and state
# level data to exist. This function is commented out below as it is specific
# to a project I am working on, but illustrates how these two functions could
# work together.

list_of_searchs = ['private school', 'home school']

for i in list_of_searchs:
    google_trend(i, 'past_day', 'both',
                 download_folder=downloadfolder,
                 folder_dest=move_data_to)

    pre_process(i, move_data_to)


