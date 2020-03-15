from model import User, Carrier, Plan, PlanCoverage, UserPlan, connect_to_db, db
from process_plans import user_saved_plans, find_fips_code
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


class TestModel(unittest.TestCase):
    """Test querying from model"""

    def setUp(self):
        """Prepare for testing"""

        # Show Flask errors when running tests
        app.config['TESTING'] = True
        # app.config['SECRET_KEY'] = 'TEMP'

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Execute after every test ends"""

        db.session.close()
        db.drop_all()

    # test querying data from database
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

    def test_find_plan_coverage(self):
        """Find plan coverage in test database"""
        
        plan_cov_1 = PlanCoverage.query.filter(
                        PlanCoverage.pcp == 
                        'In-Network: $15 / Out-of-Network: Not Covered').first()
        self.assertEqual(plan_cov_1.pcp, 
                         'In-Network: $15 / Out-of-Network: Not Covered')                        

    def test_find_user_plan(self):
        """Find user plan in test database"""
        
        user_plan_1 = UserPlan.query.filter(UserPlan.user_id == 1).first()
        self.assertEqual(user_plan_1.user_id, 1)

    # test function call to query all user plans
    def test_user_saved_plans(self):
        """Test return all user's saved plans"""

        user_plans = user_saved_plans(1)
        plans = Plan.query.all()
        self.assertEqual(user_plans, plans)


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes where user isn't logged in"""

    def setUp(self):
        """Prepare for testing"""

        # Create Flask test client
        self.client = app.test_client()

        # Show Flask errors when running tests
        app.config['TESTING'] = True


    def test_index(self):
        """Test homepage when user is not logged in"""
        
        result = self.client.get('/')
        self.assertIn(b"<h1>What's My CARE</h1>", result.data)


    def test_register(self):
        """Test register page is correct"""

        result = self.client.get('/register')
        self.assertIn(b'<h2>Register here</h2>', result.data)


    def test_login(self):
        """Test login page is correct"""
        
        result = self.client.get('/login')
        self.assertIn(b'<h2>Login</h2>', result.data)


class FlaskTestsLoggedIn(unittest.TestCase):
    """Test Flask Routes where user is logged in"""

    def setUp(self):
        """Prepare for testing"""

        # Get Flask test client
        self.client = app.test_client()

        # Show Flask errors when running tests
        app.config['TESTING'] = True
        # app.config['SECRET_KEY'] = 'TEMP'

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        # Create mock
        def _mock_find_fips_code(fips_code):
            return '06041'

        find_fips_code = _mock_find_fips_code

    def tearDown(self):
        """Execute after every test ends"""

        db.session.close()
        db.drop_all()


    # def test_post_register(self):
    #     """Test register redirects when user without an account registers"""

    #     client = app.test_client()

    #     result = client.post('/register', 
    #                         data={'email': 'jim@gmail.com',
    #                               'password': 'test',
    #                               'market': 'individual',
    #                               'zip_code': '94960'},
    #                         follow_redirects=True)

    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'<h3>User Information</h3>', result.data)


    # def test_add_user(self):
    #     """Test add_user function to see if user is correctly saved into 
    #     database when user registers
    #     """

    #     fips_code = mock_find_fips_code('94960')
    #     self.assertEqual(fips_code, '06041')

    #     new_user = User(email='jim@gmail.com', 
    #                     password='test', 
    #                     market='individual', 
    #                     zip_code='94960',
    #                     fips_code=fips_code)

    #     jim = User.query.filter(User.email == 'jim@gmail.com').first()
    #     self.assertEqual(jim.email, 'jim@gmail.com')
    #     self.assertEqual(jim.password, 'test')
    #     self.assertEqual(jim.market, 'individual')
    #     self.assertEqual(jim.zip_code, '94960')


    def test_post_login(self):
        """Test login page when user submits information, should redirect to 
        homepage
        """

        result = self.client.post('/login',
                                  data={'email': 'sarah@gmail.com',
                                        'password': 'test'},
                                  follow_redirects=True)

        self.assertEqual(result.status_code, 200)                                   
        self.assertIn(b'<h3>User Information</h3>', result.data)


    def test_logout(self):
        """Test log out page"""

        result = self.client.get('/logout', follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)                                   
        self.assertIn(b"<h1>What's My CARE</h1>", result.data)


    def test_search_plans(self):
        """Test search plans route is the correct page"""
        
        result = self.client.get('/search_plans')
        self.assertIn(b'<h3>Find Plans</h3>', result.data)

    # def test_search_plans_json(self):
    #     """Test search plans json route"""

    #     result = self.client.get('/show_plans.json', data={'age': '25',
    #                                                        'smoker': 'false',
    #                                                        'child': 'false'})


    def test_search_providers(self):
        """Test search providers route is the correct page"""

        result = self.client.get('/get_providers')
        self.assertIn(b'<h3>Find Providers</h3>', result.data)


    # def test_search_providers_json(self):
    #     pass




if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
