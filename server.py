from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Carrier, Plan, PlanType

app = Flask(__name__)

app.secret_key = "TEMP"

# Raises errors for debugging
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")

@app.route('/register', methods=['GET']) 
def register_form():
    """Show form for user to signup"""
    pass
    # return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_process():
    """Process registration"""
    pass

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""
    pass

@app.route('/login', methods=['POST'])
def login_process():
    """Process login"""
    pass

@app.route('/logout')
def logout():
    """Log out"""
    pass




if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    #     DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(host="0.0.0.0")