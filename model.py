from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User looking to seek healthcare"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)   
    age = db.Column(db.Integer, nullable=True)
    child = db.Column(db.Boolean, nullable=True)                                                           
    email = db.Column(db.String(100), nullable=False)
    market = db.Column(db.String(15), nullable=False)
    smoker = db.Column(db.Boolean, nullable=True)
    fips_code = db.Column(db.String(6), nullable=False)
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
                                

class Coverage(db.Model):
    """Plan's coverage information for in-network and out-of-network"""

    __tablename__ = "coverages"

    coverage_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    in_network = db.Column(db.String(250), nullable=False)
    out_of_network = db.Column(db.String(250), nullable=True)
    cost = db.Column(db.Integer, nullable=True)
    

    def __repr__(self):

        return f"""<Coverage coverage_id={self.coverage_id}
                    in_network={self.in_network}
                    out_of_network={self.out_of_network}>"""


class Service(db.Model):
    """Specific type of service in the Benefits Plan"""

    __tablename__ = "services" 

    service_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    service_type = db.Column(db.String(64),nullable=False)   

    def __repr__(self):

        return f"<Service service_id={self.service_id} \
                          service_type={self.service_type}>"


class Plan(db.Model):
    """Create relation between Coverage, Service and Carrier"""

    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    coverage_id = db.Column(db.Integer, 
                            db.ForeignKey('coverages.coverage_id'), index=True)
    service_id = db.Column(db.Integer, 
                           db.ForeignKey('services.service_id'), index=True)
    carrier_id = db.Column(db.Integer,
                           db.ForeignKey('carriers.carrier_id'), index=True)


    # Define relationship to coverage
    coverage = db.relationship("Coverage", 
                               backref=db.backref("plans", order_by=plan_id))

    # Define relationship to service
    service = db.relationship("Service", 
                              backref=db.backref("plans", order_by=plan_id))

    # Define relationship to carrier
    carrier = db.relationship("Carrier",
                              backref=db.backref("plans", order_by=plan_id))

# may not need association tables below:
# class UserCarrier(db.Model):
#     """Create relation between User and Carrier"""

#     __tablename__ = "usercarriers"

#     usercarrier_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
#     carrier_id = db.Column(db.Integer, 
#                            db.ForeignKey('carriers.carrier_id'), index=True)

#     # Define relationship to user
#     user = db.relationship("User", backref=db.backref("usercarriers", 
#                                    order_by=usercarrier_id)) 

#     # Define relationship to carrier
#     carrier = db.relationship("Carrier", backref=db.backref("usercarriers",
#                                          order_by=usercarrier_id))       


# class User_Cost(db.Model):
#     """Create relation between User and Plan, includes cost for user per plan"""

#     __tablename__ = "user_costs"

#     user_cost_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     cost = db.Column(db.Integer, nullable=False)
#     plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), index=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)

                                       
    # def __repr__(self):

    #     return f"<User Cost cost_id={self.cost_id} cost={self.cost}>"

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
