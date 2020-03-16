from model import User, Carrier, Plan, PlanCoverage, UserPlan, connect_to_db, db
from process_plans import user_saved_plans, find_fips_code
from server import app
from seed import add_carrier, add_plan_coverage
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
    """Test database related functions"""

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


    def test_user_saved_plans(self):
        """Test function call to return all user's saved plans"""

        user_plans = user_saved_plans(1)
        plans = Plan.query.all()
        self.assertEqual(user_plans, plans)


    def test_add_new_carrier(self):
        """Test function call to save new carrier to database"""

        ex_carrier_data = {'id': '10544CA0080001',
                           'carrier_name': 'Oscar',
                           'display_name': 'Oscar Minimum Coverage EPO',
                           'plan_type': 'EPO'}

        saved_carrier = add_carrier(ex_carrier_data)
        self.assertEqual(saved_carrier.name, 'Oscar')


    def test_add_old_carrier(self):
        """Test function to save old carrier to database, should not save 
        duplicate
        """

        ex_carrier_data = {'id': '10544CA0080001',
                           'carrier_name': 'Kaiser Permanente',
                           'display_name': 'Bronze 60 HDHP HMO',
                           'plan_type': 'HMO'}

        saved_carrier = add_carrier(ex_carrier_data)
        self.assertEqual(saved_carrier.name, 'Kaiser Permanente')

        carrier = Carrier.query.filter(Carrier.name == 'Kaiser Permanente').all()
        self.assertEqual(len(carrier), 1)

    
    def test_add_plan_coverage(self):
        """Test function to save plan coverage to database"""

        example_pc_data = {
            'pcp': 'In-Network: first 3 visit(s) $0 then $0 after deductible / Out-of-Network: Not Covered', 
            'specialist': 'In-Network: $0 after deductible / Out-of-Network: Not Covered', 
            'emerg_rm': 'In-Network: $0 after deductible / Out-of-Network: $0 after deductible', 
            'gen_drug': 'In-Network: $0 after deductible / Out-of-Network: Not Covered', 
            'urg_care': 'In-Network: first 3 visit(s) $0 then $0 after deductible / Out-of-Network: first 3 visit(s) $0 then $0 after deductible',
            'med_deduct': 'In-Network: $8,150 / Out-of-Network: Not Covered', 
            'med_moop': 'In-Network: $8,150 / Out-of-Network: Not Covered'
            }

        saved_pc = add_plan_coverage(example_pc_data)
        self.assertEqual(saved_pc.med_moop, 
                         'In-Network: $8,150 / Out-of-Network: Not Covered')

    def test_remove_plan(self):
        """Test function to remove plan associated with user and from database 
        because there is no more relationship with other users
        """

        pass


    def test_check_remove_plan(self):
        """Test remove_plan function to remove plan associated with user, but
        not from database because there is still relationship with another user
        """

        pass


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


    # def test_seed_plans(self):
    #     """Test if the selected plan is saved into database"""

    #     pass

    def test_remove_userplan(self):
        """Test if the selected plan is removed and return correct message"""
        
        result = self.client.post('/remove_plan', 
                                  data={'planId': '64210CA0620001'})
                                        

        self.assertIn(b'Plan successfully removed.', result.data)



if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
