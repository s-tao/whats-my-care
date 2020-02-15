"""Processing healthcare plans"""

from model import User
import os
import requests
import json



header = {'Accept': 'application/json',
          'apikey': os.environ['YOUR_API_KEY']}
          


def find_fips_code(user):
    """Use user zip code to return county fips code"""
    
    url = f'https://marketplace.api.healthcare.gov/api/v1/counties/by/zip/{user.zip_code}'
    
    req = requests.get(url, headers=header)
    print(req.url, "url")

    req = req.json()
    print(req)

    counties = req['counties'][0]
    fips_code = counties.get('fips')
    
    print(fips_code, "fips code \n\n\n")

    return fips_code
    

def show_medical_plans(user):
    """Use user input to return all qualified medical plans"""

    countyfips = find_fips_code(user)
    # headers = {'apikey': os.environ['YOUR_API_KEY'],
    #            'Accept': 'application/json'}

    url = 'https://marketplace.api.healthcare.gov/api/v1/plans/search'
    
    # Display # of insurance plans (every 10)
    offset = 0

    data = {"market": user.market,
            "offset": offset,
            "place": {
                "countyfips": countyfips,
                "state": user.state,
                "zipcode": user.zip_code
                }
           }
    
    req = requests.post(url, data=json.dumps(data), headers=header)

    return req.json()


def parse_med_plans(medical_plans):
#     """Reduce all data in plans to most commonly requested services"""
    pass
#     # need carrier_name
#     # need display_name
#     # need id 

#     condensed_data = {}

#     for data in medical_plans['plans']:
#         condensed_data['ambulance'] = data.get('ambulance')
#         condensed_data['carrier_name'] = data.get('carrier_name')
        
#         return data


