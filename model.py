from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Users looking to seek healthcare"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)   
    age = db.Column(db.Integer, nullable=False)
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)

    #Define relationship to user
    user = db.relationship("User", 
                           backref=db.backref("carriers", order_by=carrier_id))

    def __repr__(self):

        return f"<Carrier carrier_id={self.carrier_id} name={self.name}>"
                                

class Coverage(db.Model):
    """Benefit's coverage information for in-network and out-of-network"""

    __tablename__ = "coverages"

    coverage_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    in_network = db.Column(db.String(150), nullable=True)
    out_of_network = db.Column(db.String(150), nullable=True)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carriers.carrier_id'), 
                           index=True)
    benefits_id = db.Column(db.Integer, db.ForeignKey('benefits_fields.benefits_id'),
                            index=True)

    #Define relationship to carrier

    #Define relationship to benefit


    def __repr__(self):

        return f"""<Coverage coverage_id={self.coverage_id}
                    in_network={self.in_network}
                    out_of_network={self.out_of_network}>"""


class Benefits_Field(db.Model):
    """Specific type of service in the Benefits Plan"""

    __tablename__ = "benefits_fields" 

    benefits_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    benefits_type = db.Column(db.String(64),nullable=False)   

    def __repr__(self):

        return f"<Benefits_Field benefits_id={self.benefits_id} 
                                 benefits_type={self.benefits_type}>"

                        
class User_Cost(db.Model):
    """User's cost based off their qualifications, selected plan and coverage"""

    __tablename__ = "user_costs"

    cost_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cost = db.Column(db.Integer, nullable=False)
    benefits_id = db.Column(db.Integer, db.ForeignKey('benefits_fields.benefits_id'),
                            index=True)

    #define relationship to benefit


    def __repr__(self):

        return f"<User Cost cost_id={self.cost_id} cost={self.cost}>"


class Provider(db.Model):
    """Providers that accepts the type of Benefit's coverage plan"""

    __tablename__ = "providers"

    provider_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location = db.Column(db.String(25), nullable=False)
    company = db.Column(db.String(25), nullable=True)
    specialty = db.Column(db.String(30), nullable=True)
    # coverage_id = db.Column(db.Integer, db.ForeignKey('coverages.coverage_id'),
    #                                     index=True)

    def __repr__(self):

        return f"<Provider provider_id={self.provider_id} location={self.location}>"                                    

                                                        
class ProviderCoverage(db.Model):
    """Connecting the Provider and Coverage tables to set many-to-many relation"""

    __tablename__ = "providercoverages"

    provider_id = db.Column(db.Integer, db.ForeignKey('providers.provider_id'),
                            index=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey('coverages.coverage_id'),
                            index=True)  

    #define relationship to provider?

    #define relationship to coverage?

class Specialty(db.Model):
    """Specialties that each Provider offers"""

    __tablename__ = "specialties"

    specialty_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(25), nullable=True)
    # provider_id = db.Column(db.Integer, db.ForeignKey('providers.provider_id'),
    #                                     index=True)

    def __repr__(self):

        return f"<Specialty specialty_id={self.specialty_id} name={self.name}>"


class ProviderSpecialty(db.Model):
    """Connecting Provider and Specialty tables to set many-to-many relation"""

    __tablename__ = "providerspecialties"

    provider_id = db.Column(db.Integer, db.ForeignKey('providers.provider_id'),
                            index=True)

    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.specialty_id'),
                             index=True)  

    #define relationship to provider?

    #define relationship to specialty?


