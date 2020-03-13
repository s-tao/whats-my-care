# What's My CARE

What's My CARE is a full-stack web application that allows users to input their 
information to see all the insurance plans that they can qualify for. Users can 
save as many insurance plans as they choose to and remove any plans that they 
are no longer interested in. Users can also find providers who accepts their 
saved plans.

This project was created in February 2020 in the course of four weeks, at an 
all-female coding bootcamp, Hackbright Academy. 

### Contents

* [Tech Stack](#techstack)
* [Installation](#install)
* [Features](#features)
* [Future Features](#future-features)

## <a name=techstack></a>Tech Stack

**Backend |** Python, Flask, Jinja, SQLAlchemy, PostgreSQL
**Frontend |** Javascript, jQuery, AJAX, HTML, CSS, Foundation
**APIs |** Vericred, Google Maps Javascript

## <a name=install></a>Installation

Create a file `secrets.sh` to store your API keys for [Vericred](https://developers.vericred.com/) 
and [Google Maps Javascript](https://developers.google.com/maps/documentation/javascript/tutorial)
```
export VERICRED='YOUR_KEY'
export GOOGLE_MAPS_JS='YOUR_KEY'
```
You can also opt to restrict Google Maps Javascript API rather than saving the
key into `secrets.sh`

Clone What's My CARE repository:
`$ git clone https://github.com/s-tao/whats-my-care.git`
Create a virtual environment in the directory
`$ virtualenv env`
Activate virtual environment
`$ source env/bin/activate`
Install dependencies 
`$ pip3 install -r requirements.txt`
Create database
`$ createdb healthcare`
Run `seed.py` to create your database tables
`$ python3 seed.py`
Source your `secrets.sh`
`$ source secrets.sh`
Run the app
`$ python3 server.py`
Open localhost:5000 on your browser

## <a name=features></a>Features


## <a name=future-features></a>Future Features