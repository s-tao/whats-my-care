"""Processing healthcare plans"""
from model import User, Carrier, Plan, UserPlan, PlanCoverage
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



def show_medical_plans(user, age=None, smoker=None, child=None):
    """Show all medical plans based on user's location"""

    url = 'https://api.vericred.com/plans/search'

    payload = {'zip_code': user.zip_code,
                'fips_code': user.fips_code, 
                'market': user.market,
                'applicants': [
                    {'age': age,
                    'child': child,
                    'smoker': smoker
                    }
                  ],
                'sort': 'premium:asc'}

    if not (age and smoker and child):
        del payload['applicants']
        payload['sort'] = 'level:asc'


    req = requests.post(url, json=payload, headers=HEADERS)
    all_plans = req.json()

    all_extracted_plans = []

    for plan in all_plans['plans']:

        extracted_plan_data = parse_med_plans(plan)
        all_extracted_plans.append(extracted_plan_data)

    return all_extracted_plans


def search_medical_plan(plan_ids):
    """Find a specific plan through plan id"""

    plan_datas = []

    for plan_id in plan_ids:

        url = f'https://api.vericred.com/plans/medical/{plan_id}'

        req = requests.get(url, headers=HEADERS)
   
        extracted_plan_data = parse_single_med_plan(req.json())

        plan_datas.append(extracted_plan_data)

    return plan_datas


def parse_med_plans(plan):
    """Parse through plans to only show specific information"""
      
    extracted_plan = {}

    # specific plan information
    extracted_plan['id'] = plan.get('id')
    extracted_plan['carrier_name'] = plan.get('carrier_name')
    extracted_plan['display_name'] = plan.get('display_name')
    extracted_plan['plan_type'] = plan.get('plan_type')

    # common services
    extracted_plan['pcp'] = plan.get('primary_care_physician')
    extracted_plan['specialist'] = plan.get('specialist')
    extracted_plan['emerg_rm'] = plan.get('emergency_room')
    extracted_plan['gen_drug'] = plan.get('generic_drugs')
    extracted_plan['urg_care'] = plan.get('urgent_care')

    # overall deductible costs
    extracted_plan['med_deduct'] = plan.get('individual_medical_deductible')
    extracted_plan['med_moop'] = plan.get('individual_medical_moop')
    extracted_plan['premium'] = plan.get('premium')

    if extracted_plan['premium'] == 0:
        extracted_plan['premium'] = 'N/A'
        
    return extracted_plan


def parse_single_med_plan(plan):
    """Parse through single plan to only show specific information"""
      
    extracted_plan = {}

    # specific plan information
    extracted_plan['id'] = plan['plan'].get('id')
    extracted_plan['carrier_name'] = plan['plan'].get('carrier_name')
    extracted_plan['display_name'] = plan['plan'].get('display_name')
    extracted_plan['plan_type'] = plan['plan'].get('plan_type')

    # common services
    extracted_plan['pcp'] = plan['plan'].get('primary_care_physician')
    extracted_plan['specialist'] = plan['plan'].get('specialist')
    extracted_plan['emerg_rm'] = plan['plan'].get('emergency_room')
    extracted_plan['gen_drug'] = plan['plan'].get('generic_drugs')
    extracted_plan['urg_care'] = plan['plan'].get('urgent_care')

    # overall deductible costs
    extracted_plan['med_deduct'] = plan['plan'].get('individual_medical_deductible')
    extracted_plan['med_moop'] = plan['plan'].get('individual_medical_moop')
    extracted_plan['premium'] = plan['plan'].get('premium')

    if extracted_plan['premium'] == 0:
        extracted_plan['premium'] = 'N/A'

    return extracted_plan


def user_saved_plans(user_id):
    """Return all user's saved plans"""

    user_plans = UserPlan.query.filter(UserPlan.user_id == user_id).all()

    plans = []

    for plan in user_plans:
        p = Plan.query.filter(Plan.plan_id == plan.plan_id).first()
        plans.append(p)

    return plans


def temp_data_call():
    """Temporarily return plans for testing"""
    medical_plans = all_plans()

    return medical_plans['plans']



