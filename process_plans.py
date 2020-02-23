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

    # return json file as itself to access total plans for pagination - 
    # json[meta]['total']
    # and to access plans dictionary json['plans']
    return req.json() 


def search_medical_plan(plan_ids):
    """Find a specific plan through plan id"""

    plan_datas = []

    for plan_id in plan_ids:

        url = f'https://api.vericred.com/plans/medical/{plan_id}'

        req = requests.get(url, headers=HEADERS)

        print(req.url, "req.url")
        print(req)

        extracted_plan_data = parse_med_plans(req.json())

        plan_datas.append(extracted_plan_data)

    return plan_datas


def parse_med_plans(plan):
    """Temporarily return plans for testing"""
      
    extracted_data = {}

    # specific plan information
    extracted_data['id'] = plan['plan'].get('id')
    extracted_data['carrier_name'] = plan['plan'].get('carrier_name')
    extracted_data['display_name'] = plan['plan'].get('display_name')
    extracted_data['plan_type'] = plan['plan'].get('plan_type')

    # common services
    extracted_data['primary_care_physician'] = plan['plan'].get('primary_care_physician')
    extracted_data['specialist'] = plan['plan'].get('specialist')
    extracted_data['emergency_room'] = plan['plan'].get('emergency_room')
    extracted_data['generic_drugs'] = plan['plan'].get('generic_drugs')
    extracted_data['urgent_care'] = plan['plan'].get('urgent_care')

    # overall deductible costs
    extracted_data['individual_medical_deductible'] = plan['plan'].get('individual_medical_deductible')
    extracted_data['individual_medical_moop'] = plan['plan'].get('individual_medical_moop')

    return extracted_data


def temp_data_call():
    """Temporarily return plans for testing"""
    medical_plans = all_plans()

    return medical_plans['plans']
