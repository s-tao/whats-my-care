"""Processing healthcare plans"""

from model import User
import os
import requests
from temp_seed import all_plans


HEADERS = {'Content-Type': 'application/json',
           'Vericred-Api-Key': os.environ['YOUR_API_KEY']}
          


def find_fips_code(user):
    """Use user zip code to return county fips code"""

    url = 'https://api.vericred.com/zip_counties'

    payload = {"zip_prefix": user.zip_code}

    req = requests.get(url, params=payload, headers=HEADERS)
    req = req.json()

    counties = req['counties'][0]

    fips_code = counties.get('fips_code')

    return fips_code



def show_medical_plans(user):
    """Show all medical plans based on user's location"""
    fips_code = find_fips_code(user)

    url = 'https://api.vericred.com/plans'

    payload = {'zip_code': user.zip_code,
               'fips_code': fips_code, 
               'market': user.market}

    req = requests.get(url, params=payload, headers=HEADERS)

    return req.json() 


def parse_med_plans():
    """Reduce all data in plans to most commonly requested services"""
    medical_plans = all_plans()


    # need carrier_name
    # need display_name
    # need id 

    condensed_data = {}

    for data in medical_plans['plans']:
        # condensed_data['ambulance'] = data.get('ambulance')
        condensed_data['id'] = data.get('id')
        condensed_data['carrier_name'] = data.get('carrier_name')
        condensed_data['display_name'] = data.get('display_name')
        condensed_data['plan_type'] = data.get('plan_type')
        condensed_data['primary_care_physician'] = data.get('primary_care_physician')
        condensed_data['specialist'] = data.get('specialist')
        condensed_data['emergency_room'] = data.get('emergency_room')
        condensed_data['generic_drugs'] = data.get('generic_drugs')
        condensed_data['inpatient_facility'] = data.get('inpatient_facility')
        condensed_data['urgent_care'] = data.get('urgent_care')
        condensed_data['individual_medical_deductible'] = data.get('individual_medical_deductible')
        condensed_data['individual_medical_moop'] = data.get('individual_medical_moop')

    
    return condensed_data


