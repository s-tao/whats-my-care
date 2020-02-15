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

    all_revised_plans = []

    # loop through to add items to specific plan nested dict.
    for data in medical_plans['plans']:

        individual_plan = {}
        
        # specific plan information
        individual_plan['id'] = data.get('id')
        individual_plan['carrier_name'] = data.get('carrier_name')
        individual_plan['display_name'] = data.get('display_name')
        individual_plan['plan_type'] = data.get('plan_type')
        
        # common services
        individual_plan['primary_care_physician'] = data.get('primary_care_physician')
        individual_plan['specialist'] = data.get('specialist')
        individual_plan['emergency_room'] = data.get('emergency_room')
        individual_plan['generic_drugs'] = data.get('generic_drugs')
        # individual_plan['inpatient_facility'] = data.get('inpatient_facility')
        individual_plan['urgent_care'] = data.get('urgent_care')
        

        # overall deductible costs
        individual_plan['individual_medical_deductible'] = data.get('individual_medical_deductible')
        individual_plan['individual_medical_moop'] = data.get('individual_medical_moop')

        all_revised_plans.append(individual_plan)
    
    return all_revised_plans


