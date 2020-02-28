"""Processing provider search"""
from model import User, UserPlan, Plan
import os
import requests
import json
from temp_seed_providers import all_providers

HEADERS = {'Content-Type': 'application/json',
        #    'Accept-Version': 'v7',
           'Vericred-Api-Key': os.environ['YOUR_API_KEY']}
          

def find_providers(zip_code, radius, plan_id, user_id, search_term=None):
    """Use user input to show all qualifying providers"""

    if not zip_code:
        user = User.query.filter(User.user_id == user_id).first()
        zip_code = user.zip_code

    url = 'https://api.vericred.com/providers/search'

    # include specialty item in search
    # convert to plan_id list for rest api
    payload = {
               'plan_ids': [plan_id],
               'search_term': search_term,
               'radius': int(radius),
               'zip_code': zip_code,
               'sort': 'distance'
              }

              
    req = requests.post(url, json=payload, headers=HEADERS)

    all_providers = req.json()
    
    return all_providers


def temp_provider_call():
    """Temporarily return providers for testing"""

    providers = all_providers()

    return providers['providers']    
