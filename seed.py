from sqlalchemy import func

from model import User, Carrier, Plan, PlanType, connect_to_db, db
from process_plans import find_fips_code


def add_user(email, password, market, zip_code):
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

if __name__ == "__main__":
    # connect_to_db(app)
    db.create_all()



 