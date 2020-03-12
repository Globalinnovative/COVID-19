# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a python script to see how a Country is performing the managment of the COVID-19 cases
"""

import requests
import pandas as pd
from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np
from countryinfo import CountryInfo
import os
import re


def make_graph(country, start_date, show_score = False):
    header = ['Province/State','Country/Region','Last Update','Confirmed','Deaths','Recovered','Latitude','Longitude']
    countries_split_in_provinces =  ['US', 'Mainland China', 'Canada', 'Australia']
    provincies = ['Hubei','Guangdong','Henan','Zhejiang','Hunan','Anhui','Jiangxi','Shandong','Chongqing','Sichuan','Heilongjiang','Beijing','Shanghai','Hebei','Yunnan','Shaanxi','Fujian','Guangxi','Jiangsu','Guizhou','Hainan','California','New York','Washington','Indiana']
    raw_link = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'
    end_date = date.today()
    delta = end_date - start_date
    graph_path = os.path.join(os.path.dirname(__file__), 'graph')
    data = list()
    
    if show_score:
        try:
            population = CountryInfo(country).population()
        except:
            country_correction = {'US': 'United States','Mainland China':'China'}
            population = CountryInfo(country_correction[country]).population()
    
    for i in range(delta.days):
        day = (start_date + timedelta(days=i))
        str_day = day.strftime('%m-%d-%Y')
        r = requests.get(raw_link.format(str_day))
        sub_data = list()
        
        if day > date(2020, 3, 10):
            # they changed the name
            if country == 'Mainland China': country = 'China'
        
        if r.status_code == 404:
            break
        
        if country in countries_split_in_provinces:
            sub_total = {'posit':0, 'death':0, 'recov':0}
            
        matches = len(re.findall(country, r.text))
        if matches == 0:
            continue
        elif matches == 1:
            country_has_provincies = False
        else:
            country_has_provincies = True
            sub_total = {'posit':0, 'death':0, 'recov':0}
            
        
        rows = r.text.splitlines()
        for row in rows:
            row_slice = row.split(',')
            # Some country have a comma that creates troubble
            if len(row_slice) == 7 or len(row_slice) == 9:
                row_slice[0:2] = [''.join(row_slice[0:2])]
            
            if country in provincies:
                if re.match(country, row_slice[0]):
                    sub_data = row_slice
            else:   
                if country_has_provincies is False:
                    if re.match(country, row_slice[1]):
                        sub_data = row_slice
                else:
                    if re.match(country, row_slice[1]):
                        sub_data = row_slice
                    
                        if country_has_provincies:
                            sub_total['posit'] += int(sub_data[3])
                            sub_total['death'] += int(sub_data[4])
                            sub_total['recov'] += int(sub_data[5])

        if len(sub_data) == 0:
            continue
        else:
            sub_data[2] = str_day[:5]

            if country_has_provincies:
                sub_data[3] = sub_total['posit']
                sub_data[4] = sub_total['death']
                sub_data[5] = sub_total['recov']
        
        data.append(sub_data)
        
    if len(data) == 1: # skip dataframe with only one entry
        return
    
    df = pd.DataFrame(data, columns=header)
    df = df.drop(columns= ['Province/State','Country/Region','Latitude', 'Longitude'])
    #df = df.drop(columns= ['Latitude', 'Longitude'])

    df['Confirmed'] = df['Confirmed'].astype('int')
    df['Recovered'] = df['Recovered'].astype('int')
    df['Deaths'] = df['Deaths'].astype('int')
    df.at[0, 'Positives'] = df.at[0,'Confirmed'] - (df.at[0,'Recovered'] + df.at[0,'Deaths'])
    
    begin_of_data = True
    for i in range(1, df.shape[0]):
        # Today
        t_confirmed = df.at[i,'Confirmed']
        t_recovered = df.at[i,'Recovered']
        t_deaths = df.at[i,'Deaths']
        t_positives = t_confirmed - (t_recovered + t_deaths)
        df.at[i, 'Positives'] = t_positives
        
        # Yesterday
        try:
            y_confirmed = df.at[i-1,'Confirmed']
            y_recovered = df.at[i-1,'Recovered']
            y_deaths = df.at[i-1,'Deaths']
        except:
            pass
        
        # Daily
        d_confirmed = t_confirmed - y_confirmed
        d_recovered = t_recovered - y_recovered
        d_deaths = t_deaths - y_deaths
        
        if begin_of_data:
            # delete row if nothing happened at the beginning of the data
            if d_confirmed == 0 and d_recovered == 0 and d_deaths == 0:
                if 0 in df.index:
                    df = df.drop(0, axis=0)
                df = df.drop(i, axis=0)
            else:
                begin_of_data = False
        else:
            df.at[i, 'D-Confirmed'] = d_confirmed
            df.at[i, 'D-Recovered'] = d_recovered
            df.at[i, 'D-Deaths'] = d_deaths
        
        if show_score:
            # Edits for the score calulation
            if d_recovered <= 0: d_recovered = 0.1
            if d_confirmed <= 0: d_confirmed = 0.1
            if d_deaths <= 0: d_deaths = 0.1
            df.at[i, 'Score'] = round((d_recovered/t_positives)/((d_confirmed/(population/10000)) * (d_deaths/t_positives)))    

    if df.empty:
        return
    
    df = df.fillna(0)
    df['Positives'] = df['Positives'].astype('int')
    df['D-Confirmed'] = df['D-Confirmed'].astype('int')
    df['D-Recovered'] = df['D-Recovered'].astype('int')
    df['D-Deaths'] = df['D-Deaths'].astype('int')
    if show_score:
        df['Score'] = df['Score'].astype('int')
    
    #print(df.to_string())
    
    bar_width = 0.2
    opacity = 0.7
    steps = bar_width * 3 + bar_width # between a group of three bars
    index = np.arange(0, df.shape[0]/(1/steps), steps) # position of the x-element on the plot
    
    fig, ax1 = plt.subplots()
    plt.xticks(index, df['Last Update'].to_list(), rotation=45)
    plt.xlabel('Date')
    plt.title('COVID-19 Infections in {}'.format(country))
    
    # Axis 1: Cases
    ax1.set_ylabel('Cases')
    ax1.bar(index, df['D-Confirmed'].to_list(), bar_width, color='b', alpha=opacity, label='Confirmed')
    ax1.bar(index + bar_width, df['D-Recovered'].to_list(), bar_width, color='g', alpha=opacity, label='Recovered')
    ax1.bar(index + bar_width * 2, df['D-Deaths'].to_list(), bar_width, color='r', alpha=opacity, label='Deaths')
    
    try:
        if not os.path.exists(graph_path):
            os.mkdir(graph_path)
    except OSError:
        print('Creation of the directory failed')
        
    if show_score:
        # Axis 2: Score
        ax2 = ax1.twinx()
        ax2.set_ylabel('Score')
        ax2.plot(index, df['Score'].to_list(), color='y', alpha=opacity, label='Score')
    
        # Create a single legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        plt.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        plt.savefig(os.path.join(graph_path, '{}_score'.format(country)))
    else:
        ax1.legend(loc='upper left')
        plt.savefig(os.path.join(graph_path, country))
        
    plt.show()
    print('Graph for {} updated at {} created'.format(country, date.today()))

def main():
    start_date = date(2020, 2, 24)   # start date for the graphs
    
    # Asia
    make_graph('Mainland China', start_date)
    '''
    make_graph('Hubei', start_date)
    make_graph('Zhejiang', start_date)
    make_graph('South Korea', start_date)
    make_graph('Iraq', start_date)
    make_graph('Thailand', start_date)
    make_graph('Japan', start_date)
    make_graph('Taiwan', start_date)
    make_graph('Macau', start_date)
    make_graph('Singapore', start_date)
    make_graph('Vietnam', start_date)
    make_graph('Nepal', start_date)
    make_graph('India', start_date)
    make_graph('Hong Kong', start_date)
    make_graph('Iran', start_date)
    make_graph('Russia', start_date)
    
    # Europe
    make_graph('Italy', start_date)
    make_graph('France', start_date)
    make_graph('Spain', start_date)
    make_graph('Iceland', start_date)
    make_graph('Germany', start_date)
    make_graph('UK', start_date)
    make_graph('Finland', start_date)
    make_graph('Sweden', start_date)
    make_graph('Belgium', start_date)
  
    # Americas
    make_graph('US', start_date)
    make_graph('Canada', start_date)
    make_graph('Argentina', start_date)
    make_graph('Cambodia', start_date)
    make_graph('Peru', start_date)
    
    # Australia
    make_graph('Australia', start_date)

    # Africa
    make_graph('Egypt', start_date)

    # Score
    make_graph('Italy', start_date, True)
    make_graph('Mainland China', start_date, True)
    '''
if __name__ == "__main__":
    main()
    