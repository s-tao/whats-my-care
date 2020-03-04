from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Carrier, Plan, PlanCoverage, UserPlan
from process_plans import (show_medical_plans, parse_med_plans, find_fips_code, 
                           search_medical_plan, user_saved_plans, temp_data_call)

from process_providers import find_providers, temp_provider_call
from seed import add_user, add_plan, remove_plan
import os


app = Flask(__name__)

app.secret_key = 'TEMP'

# Raises errors for debugging
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    check_user = session.get('user_id')
    if check_user:
        return render_template('homepage.html', user_id=check_user)

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
    return redirect('/user_profile')


@app.route('/logout')
def logout():
    """Log out"""
    
    user_id = session.get('user_id')

    del session['user_id']

    flash('Successfully logged out')
    return redirect('/')


@app.route('/search_plans')
def plan_form():
    """User information with form to generate all qualifying user plans"""

    user_id = session.get('user_id')

    user = User.query.get(user_id)

    return render_template('search_plans.html', user_id=user_id, user=user)


@app.route('/show_plans.json', methods=['GET'])
def show_plans():
    """Generate all plans after selecting plan type"""
    
    user_id = session.get('user_id')

    user = User.query.get(user_id)

    # Get request from form in search_plans.html --future feature
    # plan_type = request.args.get('planOption')
    # age = request.args.get('age')
    # smoker = request.args.get('smoker')
    # child = request.args.get('child')



    # Return medical plans based off user's zip code and fips code
    # TEMP COMMENTING OUT TO BUILD FRONT END WITHOUT CALLING
    # plans = show_medical_plans(user, age, smoker, child)
        
    plans = temp_data_call()

    return jsonify(plans)


@app.route('/get_providers')
def get_providers():
    """Form submittal to search providers"""

    user_id = session.get('user_id')

    user_plans = UserPlan.query.filter(UserPlan.user_id == user_id).all()

    return render_template('search_providers.html', user_id=user_id,
                                                    plans=user_plans)


@app.route('/show_providers.json', methods=['GET'])
def show_providers():
    """Generate all provider information after submitting form"""
    
    user_id = session.get('user_id')

    plan_id = request.args.get('planId')
    zip_code = request.args.get('zipCode')
    radius = request.args.get('radius')
    provider_type = request.args.get('providerType')
    search_term = request.args.get('searchTerm')
    # TEMP COMMENTING OUT TO BUILD FRONT END WITHOUT CALLING
    # print(plan_id, "plan_id", zip_code, "zipcode", radius, "radius", provider_type,
    #                 "provider_type", search_term, "search term \n\n\n")    
    # providers = find_providers(user_id, plan_id, zip_code, radius, provider_type, search_term)
    providers = temp_provider_call()
    # print(providers)

    return jsonify(providers)


@app.route('/save_plans', methods=['POST'])
def seed_plans():
    """Form action to save user's choice of plan into database"""

    user_id = session.get('user_id')

    plan_ids = request.form.keys()
    add_plan(plan_ids, user_id)

    return redirect(f'/user-{user_id}/saved_plans')


@app.route('/remove_plan', methods=['POST'])
def remove_userplan():
    """Form action to remove user's choice of plan from database"""

    user_id = session.get('user_id')
    
    v_id = request.form.get('planId')

    plan = Plan.query.filter(Plan.vericred_id == v_id).first()
       
    if plan:
        remove_plan(plan, user_id)
        return 'Plan Removed'

    return 'Unexpected Error'


@app.route('/user_profile')
def user_profile():
    """Display all user's saved plans"""

    user_id = session.get('user_id')
    
    user = User.query.get(user_id)

    user_dict = {'email': user.email,
                 'market': user.market,
                 'zip code': user.zip_code}
    
    plans = user_saved_plans(user_id)

    return render_template('user_profile.html', user_id=user_id, 
                                                user_dict=user_dict,
                                                plans=plans)


if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    # DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(host='0.0.0.0')