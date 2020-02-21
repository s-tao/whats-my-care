"""Processing healthcare plans"""

from model import User
import os
import requests
from temp_seed import all_plans


HEADERS = {'Content-Type': 'application/json',
           'Vericred-Api-Key': os.environ['YOUR_API_KEY']}
          


def find_fips_code(zip_code):
    """Use user zip code to return county fips code"""

    url = 'https://api.vericred.com/zip_counties'

    payload = {"zip_prefix": zip_code}

    req = requests.get(url, params=payload, headers=HEADERS)
    req = req.json()

    counties = req['counties'][0]

    fips_code = counties.get('fips_code')

    return fips_code



def show_medical_plans(user):
    """Show all medical plans based on user's location"""

    url = 'https://api.vericred.com/plans'

    payload = {'zip_code': user.zip_code,
               'fips_code': user.fips_code, 
               'market': user.market}

    req = requests.get(url, params=payload, headers=HEADERS)

    return req.json() 


def search_medical_plan(plan_id):
    """Find a specific plan through plan id"""
    pass



def parse_med_plans():
    """Temporarily return plans for testing"""
    medical_plans = all_plans()
  
    # return json file as itself to access total plans for pagination - 
    # json[meta]['total']
    # and to access plans dictionary json['plans']
    return medical_plans['plans']


