from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User looking to seek healthcare"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)   
    password = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    market = db.Column(db.String(15), nullable=False)
    fips_code = db.Column(db.String(5), nullable=True)
    zip_code = db.Column(db.String(5), nullable=False)


    def __repr__(self):

        return f"<User user_id={self.user_id} email={self.email}>"
                                                

class Carrier(db.Model):
    """Types of health insurance carriers"""

    __tablename__ = "carriers"

    carrier_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(25), nullable=False)


    def __repr__(self):

        return f"<Carrier carrier_id={self.carrier_id} name={self.name}>"


class Plan(db.Model):
    """User's choice of plan(s)"""

    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    plan_org = db.Column(db.String(10), nullable = True)
    name = db.Column(db.String(100), nullable=False)
    vericred_id = db.Column(db.String(25), nullable=False)
    carrier_id = db.Column(db.Integer,
                           db.ForeignKey('carriers.carrier_id'), index=True)

    # Define relationship to carrier
    carrier = db.relationship("Carrier",
                              backref=db.backref("plans", order_by=plan_id))


    def __repr__(self):

        return f"<Plan plan_id={self.plan_id} name={self.name}>"


class UserPlan(db.Model):
    """Association between User and Model many-to-many relationship"""
    
    __tablename__ = "userplans"

    userplan_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), index=True)                        

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("userplans", 
                                   order_by=userplan_id))                              

    # Define relationship to plan
    plan = db.relationship("Plan", backref=db.backref("userplans", 
                                   order_by=userplan_id))
    
    def __repr__(self):

        return f"""<Userplan userplan_id={self.userplan_id} 
                                 user_id={self.user.user_id}
                                 plan_id={self.plan.plan_id}"""


class PlanCoverage(db.Model):
    """Deductible coverages for common services in a plan"""

    __tablename__ = "plan_coverages"

    pc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pcp = db.Column(db.Text, nullable=True)  
    specialist = db.Column(db.Text, nullable=True)             
    emerg_rm = db.Column(db.Text, nullable=True)             
    gen_drug = db.Column(db.Text, nullable=True)             
    urg_care = db.Column(db.Text, nullable=True)             
    med_deduct = db.Column(db.Text, nullable=True)             
    med_moop = db.Column(db.Text, nullable=True) 
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), index=True)

    # Define relationship to plan
    plan = db.relationship("Plan", backref=db.backref("plan_coverages", 
                                   order_by=pc_id))

    def __repr__(self):

        return f"<PlanCoverage pc_id={self.pc_id} plan_id={self.plan.plan_id}>"

# future datatable
class PlanType(db.Model):
    """Type of Plan""" 

    __tablename__ = "plan_types"

    plan_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name_type = db.Column(db.String(10), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), index=True)

    # Define relationship to plan
    plan = db.relationship("Plan", 
                           backref=db.backref("plan_types", 
                           order_by=plan_type_id))


def connect_to_db(app):

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///healthcare'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Work directly with database when running module interactively
     
    from server import app

    connect_to_db(app)
    print("Connected to DB.")
    
