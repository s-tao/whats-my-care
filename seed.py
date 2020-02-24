from sqlalchemy import func

from model import User, Carrier, Plan, PlanCoverage, PlanType, connect_to_db, db
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
        
        check_carrier = Carrier.query.filter(Carrier.name == 
                                             plan_data['carrier_name']).first()
    
        if not check_carrier:
            new_carrier = Carrier(name=plan_data['carrier_name'])
            db.session.add(new_carrier)

            db.session.commit()


def add_plan(plan_ids, user_id):
    """Add plan to database when user saves plans"""

    plan_datas = search_medical_plan(plan_ids)

    # check to see if carrier from plan is in database
    add_carrier(plan_datas)

    for plan_data in plan_datas:
        check_plan = Plan.query.filter(Plan.name == 
                                       plan_data['display_name']).first()
        
        if not check_plan:
            carrier = Carrier.query.filter(Carrier.name == 
                                           plan_data['carrier_name']).first()

            new_plan = Plan(plan_org=plan_data['plan_type'],
                            name=plan_data['display_name'],
                            vericred_id=plan_data['id'],
                            user_id=user_id,
                            carrier_id=carrier.carrier_id)

            db.session.add(new_plan)

    db.session.commit()    

    add_plan_coverage(plan_datas)


def add_plan_coverage(plan_datas):
    """Add plan coverage to database when user saves plans"""

    for plan_data in plan_datas:

        plan = Plan.query.filter(Plan.vericred_id == plan_data['id']).first()
        plan_id = plan.plan_id

        new_plan_coverage = PlanCoverage(
                                pcp=plan_data['pcp'],
                                specialist=plan_data['specialist'],
                                emerg_rm=plan_data['emerg_room'],
                                gen_drug=plan_data['gen_drugs'],
                                urg_care=plan_data['urg_care'],
                                med_deduct=plan_data['med_deduct'],
                                med_moop=plan_data['med_moop'],
                                plan_id=plan_id)

        db.session.add(new_plan_coverage)

    db.session.commit()


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    db.create_all()



 