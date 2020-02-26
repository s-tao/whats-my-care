from sqlalchemy import func

from model import User, Carrier, Plan, PlanCoverage, UserPlan, connect_to_db, db
from process_plans import find_fips_code, search_medical_plan, parse_med_plans


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


def add_carrier(plan_data):
    """Add carrier to database when user saves plans"""

    check_carrier = Carrier.query.filter(Carrier.name == 
                                            plan_data['carrier_name']).first()
    print(check_carrier)
    if not check_carrier:
        new_carrier = Carrier(name=plan_data['carrier_name'])
        db.session.add(new_carrier)

        db.session.commit()
        print(new_carrier)

        return new_carrier

    return check_carrier


def add_plan(plan_ids, user_id):
    """Add plan to database when user saves plans"""

    plan_datas = search_medical_plan(plan_ids)

    for plan_data in plan_datas:

        # check to see if carrier from plan is in database
        current_carrier = add_carrier(plan_data)

        plan = Plan.query.filter(Plan.name == plan_data['display_name']).first()
        
        if not plan:

            current_pc = add_plan_coverage(plan_data)

            plan = Plan(plan_org=plan_data['plan_type'],
                            name=plan_data['display_name'],
                            vericred_id=plan_data['id'],
                            carrier_id=current_carrier.carrier_id,
                            pc_id=current_pc.pc_id)

            db.session.add(plan)

            db.session.commit()    

        add_user_plan(plan, user_id)


def add_user_plan(new_plan, user_id):
    """Add user_id and plan_id to userplans datatable"""

    new_userplan = UserPlan(user_id=user_id,
                            plan_id=new_plan.plan_id)

    db.session.add(new_userplan)
    db.session.commit()


def add_plan_coverage(plan_data):
    """Add plan coverage to database when user saves plans"""

    new_plan_coverage = PlanCoverage(
                            pcp=plan_data['pcp'],
                            specialist=plan_data['specialist'],
                            emerg_rm=plan_data['emerg_rm'],
                            gen_drug=plan_data['gen_drug'],
                            urg_care=plan_data['urg_care'],
                            med_deduct=plan_data['med_deduct'],
                            med_moop=plan_data['med_moop'])

    db.session.add(new_plan_coverage)

    db.session.commit()

    return new_plan_coverage


def remove_plan(plan, user_id):
    """Remove plan that's associated with user"""

    indiv_plan = Plan.query.filter(Plan.vericred_id == plan.vericred_id).first()
    print(indiv_plan, "indiv plan \n\n\n")
    UserPlan.query.filter(UserPlan.plan_id == indiv_plan.plan_id,
                          UserPlan.user_id == user_id).delete()

    check_plan = UserPlan.query.filter(UserPlan.plan_id == indiv_plan.plan_id).first()

    if not check_plan:

        Plan.query.filter(Plan.plan_id == indiv_plan.plan_id).delete()

        PlanCoverage.query.filter(PlanCoverage.pc_id == indiv_plan.pc_id).delete()

    db.session.commit()


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    db.create_all()



 