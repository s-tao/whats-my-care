"""Processing healthcare plans"""

# import time
# import vericred_client
# from vericred_client.rest import ApiException
# from pprint import pprint
from model import User
import os
# Configure API key authorization: Vericred-Api-Key

"""
1. Create a function that takes in required parameters to call 
.RequestPlanFind and then return appropriate data required. Figure out
pages later.

2.In server.py, post request for medical submission will call function
to pass in appropriate parameters of user choice. Also insert api call for
fips code to pass in fips code in .RequestPlanFind. Information that is 
returned can be jsonify, manipulate html and js to see how information can
be displayed.

3. in server, filter out all information to top 5 services covered

"""

def process_plan():
    url = 'https://api.vericred.com/zip_counties'
    payload = {'zip_prefix': user.zip_code,
               'market': user.market,
               ''}
    headers = {'Content-Type': 'application/json',
               'Vericred-Api-Key': os.environ['YOUR_API_KEY']}

    res = requests.get(url, param=payload, headers=headers)