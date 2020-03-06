from model import User, Carrier, Plan, PlanCoverage, UserPlan, connect_to_db, db
from server import app
import unittest


def example_data():
    """Create some sample data."""

    User.query.delete()
    Carrier.query.delete()
    Plan.query.delete()
    PlanCoverage.query.delete()
    UserPlan.query.delete()

    sarah = User(email='sarah@gmail.com', 
                 password='test', 
                 market='individual',
                 fips_code='06075',
                 zip_code='94121')

    jade = User(email='jade@gmail.com',
                password='test',
                market='small_group',
                fips_code='06113',
                zip_code='95616')

    carrier_1 = Carrier(name='Kaiser Permanente')
    carrier_2 = Carrier(name='Sutter Health Plus')

    pc_1 = PlanCoverage(
                pcp='In-Network: $0 after deductible / Out-of-Network: Not Covered',
                specialist='In-Network: $0 after deductible / Out-of-Network: Not Covered',
                emerg_rm='In-Network: $0 after deductible / Out-of-Network: $0 after deductible | limit: waived if admitted',
                gen_drug='In-Network: $0 after deductible / Out-of-Network: Not Covered',
                urg_care='In-Network: $0 after deductible / Out-of-Network: Not Covered',
                med_deduct='In-Network: $6,900 / Out-of-Network: Not Covered',
                med_moop='In-Network: $6,900 / Out-of-Network: Not Covered')

    pc_2 = PlanCoverage(
                pcp='In-Network: $15 / Out-of-Network: Not Covered',
                specialist='In-Network: $30 / Out-of-Network: Not Covered',
                emerg_rm='In-Network: $150 / Out-of-Network: $150 | limit: waived if admitted',
                gen_drug='In-Network: $5 per script / Out-of-Network: Not Covered',
                urg_care='In-Network: $15 / Out-of-Network: $15',
                med_deduct='In-Network: $0 / Out-of-Network: Not Covered',
                med_moop='In-Network: $4,500 / Out-of-Network: Not Covered')

    db.session.add_all([sarah, jade, carrier_1, carrier_2, pc_1, pc_2])
    db.session.commit()

    plan_1 = Plan(plan_org='HMO',
                  name='Bronze 60 HDHP HMO',
                  vericred_id='40513CA0390019',
                  carrier_id=carrier_1.carrier_id,
                  pc_id=pc_1.pc_id)

    plan_2 = Plan(plan_org='HMO',
                  name='Platinum MI01 HMO',
                  vericred_id='64210CA0620001',
                  carrier_id=carrier_2.carrier_id,
                  pc_id=pc_2.pc_id)  

    db.session.add_all([plan_1, plan_2])
    db.session.commit()

    userplan_1 = UserPlan(user_id=sarah.user_id, plan_id=plan_1.plan_id)
    userplan_2 = UserPlan(user_id=sarah.user_id, plan_id=plan_2.plan_id)
    userplan_3 = UserPlan(user_id=jade.user_id, plan_id=plan_2.plan_id)

    db.session.add_all([userplan_1, userplan_2, userplan_3])
    db.session.commit()


class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        """Prepare for testing"""

        # Get Flask test client
        self.client = app.test_client()

        # Show Flask errors when running tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Execute after every test ends"""

        db.session.close()
        db.drop_all()

    def test_find_user(self):
        """Find user in test database"""

        sarah = User.query.filter(User.email == 'sarah@gmail.com').first()
        self.assertEqual(sarah.email, 'sarah@gmail.com')

    def test_find_carrier(self):
        """Find carrier in test database"""

        carrier_1 = Carrier.query.filter(Carrier.name == 'Kaiser Permanente').first()
        self.assertEqual(carrier_1.name, 'Kaiser Permanente')

    def test_find_plan(self):
        """Find plan in test database"""

        plan_1 = Plan.query.filter(Plan.name == 'Platinum MI01 HMO').first()
        self.assertEqual(plan_1.name, 'Platinum MI01 HMO')


    def test_index(self):
        """Test homepage"""

        # Create a test client
        client = app.test_client()

        result = client.get('/')

        self.assertIn(b"<h1>What's My Care</h1>", result.data)


    def test_login(self):
        """Test login page"""

        result = self.client.post('/login',
                                   data={'email': 'sarah@gmail.com',
                                         'password': 'test'},
                                   follow_redirects=True)
        self.assertEqual(result.status_code, 200)                                   
        self.assertIn(b'<h2>Your Information</h2>', result.data)                                   


# class FlaskTests(TestCase):
#     def setUp(self):
#         """Prepare for testing"""

#         # Get Flask test client
#         self.client = app.test_client()

#         # Show Flask errors when running tests
#         app.config['TESTING'] = True

#         # Connect to test db
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """Run when test ends"""

#         db.session.close()
#         db.drop_all()



if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
