"""Processing provider search"""
from model import User, UserPlan, Plan
import os
import requests

HEADERS = {'Content-Type': 'application/json',
        #    'Accept-Version': 'v7',
           'Vericred-Api-Key': os.environ['YOUR_API_KEY']}
          

def find_providers(zip_code, radius, plan_id, user_id):
    """Use user input to show all qualifying providers"""

    if not zip_code:
        user = User.query.filter(User.user_id == user_id).first()
        zip_code = user.zip_code

    url = 'https://api.vericred.com/providers/search'

    # convert to plan_id list for rest api
    payload = {
               'plan_ids': ["40513CA0390012", plan_id],
               'search_term': 'ENT',
               'radius': int(radius),
               'sort': 'distance',
               'zip_code': zip_code
            }

              
    req = requests.post(url, params=payload, headers=HEADERS)
    print(req.url, "url \n\n")
    all_providers = req.json()
    print(all_providers)
    
    return all_providers

