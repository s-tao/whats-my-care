from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Carrier, Plan, PlanType
from process_plans import show_medical_plans, parse_med_plans
# import requests
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
    state = request.form.get('state')
    zip_code = request.form.get('zipcode')

    user = User.query.filter(User.email == email).first()

    if user:
        flash('User account already exists.')
        return redirect('/login')

    new_user = User(email=email, 
                    password=password, 
                    market=market, 
                    state=state,
                    zip_code=zip_code)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.user_id}')


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
    return redirect(f'/users/{user.user_id}')


@app.route('/logout')
def logout():
    """Log out"""
    pass


@app.route('/users/<int:user_id>', methods=['GET'])
def user_options(user_id):
    """Main page allowing user to see plans"""

    user = User.query.get(user_id)

    user_dict = {'email': user.email,
                 'market': user.market,
                 'state': user.state,
                 'zip code': user.zip_code}
    

    return render_template('user_main.html', user=user, user_dict=user_dict)


@app.route('/users/<int:user_id>', methods=['POST'])
def all_plans(user_id):
    """Generate all plans after selecting plan type"""

    user = User.query.get(user_id)

    # Get request from form in user_main.html
    plan_type = request.form.get('choose-plan-type')

    # Return medical plans based off user's zip code and fips code
    medical_plans = show_medical_plans(user)
    # plans = parse_med_plans(medical_plans)

    return jsonify(medical_plans)


if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    #     DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(host='0.0.0.0')