"""Processing provider search"""
from model import User, UserPlan, Plan
import os
import requests
import json
from temp_seed_providers import all_providers

HEADERS = {'Content-Type': 'application/json',
        #    'Accept-Version': 'v7',
           'Vericred-Api-Key': os.environ['YOUR_API_KEY']}
          

def find_providers(user_id, plan_id, zip_code, radius, provider_type=None, 
                                                       search_term=None):
    """Use user input to show all qualifying providers"""

    if not zip_code:
        user = User.query.filter(User.user_id == user_id).first()
        zip_code = user.zip_code
        print(zip_code, "inside condition \n\n")

    url = 'https://api.vericred.com/providers/search'

    # convert to plan_id list for rest api
    payload = {
               'plan_ids': [plan_id],
               'radius': radius,
               'zip_code': zip_code,
               'sort': 'distance',
               'search_term': search_term,
               'type': provider_type
              }

    if not plan_id:
        del payload['plan_ids']

    if (not search_term) and (not provider_type):
        del payload['search_term']
        del payload['type']
    
    elif not search_term:
        del payload['search_term']

    elif not provider_type:
        del payload['type']
    
    req = requests.post(url, json=payload, headers=HEADERS)

    all_providers = req.json()
    print(all_providers)
    return all_providers.get('providers')


def temp_provider_call():
    """Temporarily return providers for testing"""

    providers = all_providers()

    return providers.get('providers')
