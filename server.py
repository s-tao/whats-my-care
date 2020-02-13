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

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration"""
    
    email = request.form.get("email")
    password = request.form.get("password")
    market = request.form.get("market")
    zip_code = request.form.get("zipcode")

    user = User.query.filter(User.email == email).first()

    if user:
        flash("User account already exists.")
        return redirect('/login')

    new_user = User(email=email, password=password, market=market, zip_code=zip_code)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.user_id}")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login"""
    
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter(User.email == email).first()

    if not user:
        flash("User does not exist")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password")
        return redirect('/login')

    session["user_id"] = user.user_id

    flash("Successfully logged in")
    return redirect(f"/users/{user.user_id}")


@app.route('/logout')
def logout():
    """Log out"""

    pass


@app.route('/users/<int:user_id>')
def user_options(user_id):
    """Main page allowing user to see plans"""

    user = User.query.get(user_id)

    user = {"email": user.email,
            "market": user.market,
            "zip code": user.zip_code}

    return render_template("user_main.html", user=user)


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    #     DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(host="0.0.0.0")