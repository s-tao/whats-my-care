from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Carrier, Plan, PlanCoverage, PlanType
from process_plans import show_medical_plans, parse_med_plans, find_fips_code, search_medical_plan, temp_data_call
from seed import add_user, add_plan
import os


app = Flask(__name__)

app.secret_key = 'TEMP'

# Raises errors for debugging
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template('homepage.html')


@app.route('/register', methods=['GET']) 
def register_form():
    """Show form for user to signup"""

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration"""
    
    email = request.form.get('email')
    password = request.form.get('password')
    market = request.form.get('market')
    zip_code = request.form.get('zipcode')

    user = User.query.filter(User.email == email).first()

    if user:
        flash('User account already exists.')
        return redirect('/login')

    # seed user information into database
    new_user = add_user(email, password, market, zip_code)
  
    return redirect(f'/user-{new_user.user_id}/show_plans')


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login_process():
    """Process login"""
    
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()

    if not user:
        flash('User does not exist')
        return redirect('/login')

    if user.password != password:
        flash('Incorrect password')
        return redirect('/login')

    session['user_id'] = user.user_id

    flash('Successfully logged in')
    return redirect(f'/user-{user.user_id}/show_plans')


@app.route('/logout')
def logout():
    """Log out"""
    
    del session['user_id']
    flash('Successfully logged out')
    return redirect('/')


@app.route('/user-<int:user_id>/show_plans', methods=['GET'])
def user_options(user_id):
    """Main page allowing user to see plans"""

    # slightly buggy --fix when bug occurs again
    if session['user_id'] != user_id:
        flash('Please login')
        return redirect('/login')

    user = User.query.get(user_id)

    user_dict = {'email': user.email,
                 'market': user.market,
                 'zip code': user.zip_code}
    

    return render_template('search_plans.html', user_id=user_id, user_dict=user_dict)


@app.route('/user-<int:user_id>/show_plans', methods=['POST'])
def all_plans(user_id):
    """Generate all plans after selecting plan type"""

    user = User.query.get(user_id)

    # Get request from form in search_plans.html --future feature
    plan_type = request.form.get('planOption')

    # Return medical plans based off user's zip code and fips code
    # TEMP COMMENTING OUT TO BUILD FRONT END WITHOUT CALLING
    medical_plans = show_medical_plans(user)
        
    # plans = temp_data_call()

    return jsonify(medical_plans) #--uncomment when running api call
    # return jsonify(plans)


@app.route('/user-<int:user_id>/saved_plans', methods=['POST'])
def seed_plans(user_id):
    
    plan_ids = request.form.keys()

    add_plan(plan_ids, user_id)


    return redirect(f'/user-{user_id}/saved_plans')


@app.route('/user-<int:user_id>/saved_plans')
def show_saved_plans(user_id):

    if session['user_id'] != user_id:
        flash('Please login')
        return redirect('/login')

    plans = Plan.query.filter(Plan.user_id == user_id).all()

    return render_template('saved_plans.html', user_id=user_id, plans=plans)


if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(host='0.0.0.0')