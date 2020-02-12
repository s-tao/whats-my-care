from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Carrier, Coverage, Service, Plan

app = Flask(__name__)

app.secret_key = "TEMP"

# Raises errors for debugging
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""

    pass