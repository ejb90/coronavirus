'''
https://coronavirus.data.gov.uk/developers-guide#methods
'''

import argparse
import requests
import datetime

import numpy as np


class GovData:
    '''
    '''
    def __init__(self, raw_data):
        self.data = raw_data['data']
        self.data.reverse()
        self.raw_dates = [dat['date'] for dat in self.data]
        self.dates = [datetime.datetime.strptime(dat['date'], '%Y-%m-%d') for dat in self.data]
        
        self.values = {}
        for key in self.data[0]:
            self.values[key] = [dat[key] for dat in self.data]
            
        
        self.rates = {}
        for key in self.values:
            if key != 'date':
                self.rates[key+'Rate'] = [0.0,] + list(np.diff(self.values[key]))
        
        self.values.update(self.rates)
        
        for key in self.values:
            print(key, len(self.values[key]))
       
       
def parse_arguments():
    '''
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')  
    
    parser.add_argument('--areaType', 
                        default='overview', 
                        choices=['overview', 'nation', 'region', 'nhsRegion', 'utla', 'ltla'],
                        help='location type')
    
    parser.add_argument('--areaName', 
                        nargs='+',
                        default=['england', 'scotland', 'wales', 'northern ireland'],
                        help='name of location')
    
    parser.add_argument('--date',
                        default=None,
                        help='pick a specific date')
    
    parser.add_argument('--metrics',
                        nargs='+',
                        default = ['date', 'newCasesByPublishDate', 'newDeaths28DaysByPublishDate'],
                        choices = ['date', 'areaName', 'newCasesByPublishDate', 'cumCasesByPublishDate', 'newAdmissions' 'cumAdmissions', 'plannedCapacityByPublishDate', 'newTestsByPublishDate', 'cumTestsByPublishDate', 'newDeaths28DaysByPublishDate', 'cumDeaths28DaysByPublishDate'])
    
    args = parser.parse_args()
    return args
    
    
def make_query(args):
    '''
    '''
    # base string to .gov data
    base_str = 'https://api.coronavirus.data.gov.uk/v1/data?'
    
    # filter string to filter data
    if args.areaType == 'overview':
        filter_str = 'filters=areaType=overview&'
    elif args.areaName is not None:
        filter_str = f'filters=areaType={args.areaType};areaName={args.areaName}&'
    else:
        raise Exception('areaType set but no areaName provided.')
    
    # get the required variables back
    metrics_str = str({met:met for met in args.metrics}).replace(' ','').replace('\'', '"')
    struct_str = f'structure={metrics_str}'
        
    endpoint = base_str + filter_str + struct_str
    return endpoint


def get_data(url):
    '''
    '''
    response = requests.get(url, timeout=10)
        
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: {response.text}')
        
    raw_data = response.json()
    data = GovData(raw_data)
    return data


def moving_average(values, width):
    '''
    '''
    average = np.convolve(values, np.ones(width), 'same') / width
    return average


def moving_average_rate(values, width):
    '''
    '''
    average = np.convolve(values, np.ones(width), 'same') / width
    rate = np.diff(average)
    rate = np.array([0.0] + list(rate))
    return rate

    

def main():
    '''
    '''
    args = parse_arguments()
    query = make_query(args)
    data = get_data(query)
    
    return args, data


if __name__ == '__main__':
    main()
    

    
