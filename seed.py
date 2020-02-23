from sqlalchemy import func

from model import User, Carrier, Plan, PlanType, connect_to_db, db
from process_plans import find_fips_code, search_medical_plan


def add_user(email, password, market, zip_code):
    """Add user information to database when user registers"""
     # only runs once when user registers to store user's fips code
    fips_code = find_fips_code(zip_code)

    new_user = User(email=email, 
                    password=password, 
                    market=market, 
                    zip_code=zip_code,
                    fips_code=fips_code)

    db.session.add(new_user)
    db.session.commit()

    return new_user


def add_carrier(plan_datas):
    """Add carrier to database when user saves plans"""

    for plan_data in plan_datas:
        
        check_carrier = Carrier.query.filter(Carrier.name == plan_data['carrier_name']).first()
    
        if not check_carrier:
            new_carrier = Carrier(name=plan_data['carrier_name'])
            db.session.add(new_carrier)

            db.session.commit()


def add_plan(plan_ids, user_id):
    """Add plan to database when user saves plans"""

    plan_datas = search_medical_plan(plan_ids)
    # plan_datas = [{'id': '40513CA0380003-04', 
    #     'carrier_name': 'Kaiser Permanente', 
    #     'display_name': 'Silver 73 HMO', 
    #     'plan_type': 'HMO', 
    #     'primary_care_physician': 'In-Network: $35 / Out-of-Network: Not Covered', 
    #     'specialist': 'In-Network: $75 / Out-of-Network: Not Covered', 
    #     'emergency_room': 'In-Network: $400 / Out-of-Network: $400 | limit: waived if admitted', 
    #     'generic_drugs': 'In-Network: $16 per script after deductible / Out-of-Network: Not Covered', 
    #     'urgent_care': 'In-Network: $35 / Out-of-Network: Not Covered', 
    #     'individual_medical_deductible': 'In-Network: $3,700 / Out-of-Network: Not Covered', 
    #     'individual_medical_moop': 'In-Network: $6,500 / Out-of-Network: Not Covered'}]
    
    # check to see if carrier from plan is in database
    add_carrier(plan_datas)

    for plan_data in plan_datas:

        carrier = Carrier.query.filter(Carrier.name == plan_data['carrier_name']).first()

        new_plan = Plan(plan_org=plan_data['plan_type'],
                        name=plan_data['display_name'],
                        vericred_id=plan_data['id'],
                        user_id=user_id,
                        carrier_id=carrier.carrier_id)

        db.session.add(new_plan)

    db.session.commit()        



if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    db.create_all()



 