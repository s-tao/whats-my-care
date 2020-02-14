"""Processing healthcare plans"""

# import time
# import vericred_client
# from vericred_client.rest import ApiException
# from pprint import pprint
from model import User
import os
import requests
import json
# Configure API key authorization: Vericred-Api-Key


HEADERS = {'Content-Type': 'application/json',
           'Vericred-Api-Key': os.environ['YOUR_API_KEY']}


def find_fips_code(user):
    url = 'https://api.vericred.com/zip_counties'
    payload = {"zip_prefix": user.zip_code}
    
    req = requests.get(url, params=payload, headers=HEADERS)
    req = req.json()
    
    counties = req['counties'][0]

    fips_code = counties.get('fips_code')

    return fips_code
    


def show_medical_plans(user, fips_code):
    url = 'https://api.vericred.com/plans'

    payload = {'zip_code': user.zip_code,
               'fips_code': fips_code, 
               'market': user.market}

    req = requests.get(url, params=payload, headers=HEADERS)

    return req.json()