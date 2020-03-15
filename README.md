# What's My CARE

What's My CARE is a full-stack web application that allows users to input their 
information to see all the insurance plans that they can qualify for. Users can 
save as many insurance plans as they choose to and remove any plans that they 
are no longer interested in. Users can also find providers who accepts their 
saved plans.

This project was created in February 2020 in the course of four weeks, at an 
all-female coding bootcamp, Hackbright Academy. 

<img src="/README_gif/front_page.png" alt="What's My CARE homepage"/>

### Contents

* [Tech Stack](#techstack)
* [Installation](#install)
* [Features](#features)
* [Future Features](#future-features)

## <a name=techstack></a>Tech Stack

**Backend |** Python, Flask, Jinja, SQLAlchemy, PostgreSQL <br>
**Frontend |** Javascript, jQuery, AJAX, HTML, CSS, Foundation <br>
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

Clone What's My CARE repository
```
$ git clone https://github.com/s-tao/whats-my-care.git
```
Create a virtual environment in the directory
```
$ virtualenv env
```
Activate virtual environment
```
$ source env/bin/activate
```
Install dependencies 
```
$ pip3 install -r requirements.txt
```
Create database
```
$ createdb healthcare
```
Run `seed.py` to create your database tables
```
$ python3 seed.py
```
Source your `secrets.sh`
```
$ source secrets.sh
```
Run the app
```
$ python3 server.py
```
Open localhost:5000 on your browser

## <a name=features></a>Features
**Login/Register** <br>
Users are prompt to login or register if they don't have an account 

Once the user logins, they're directed to the homepage where they can see all 
their saved insurance plans. 

![](/README_gif/login.gif)

**Search Plans** <br>
On the Search Plans page, users will submit their information to receive all the 
medical plans they qualify for. Currently the plans are sorted based on their 
insurance tiers if they only choose what type of plan they're looking for. If the
user submits additional information (age, smoker, child), the plans will be sorted
by premium estimates. 

![](/README_gif/search_plans.gif)

**Save Plans** <br>
User can save all the plans that interests them. 

![](/README_gif/save_plans.gif)

**Remove Saved Plans** <br>
User can also remove the plans that they're no longer interested in. 

![](/README_gif/remove_plan.gif)

**Search Providers** <br>
On the Search Providers page, users are only required to fill in the radius to 
set the distance based off their zip code for their search. They can also narrow
down their search by filling out more items. 

![](/README_gif/search_providers.gif)

User can toggle any provider information and see their corresponding location on
Google Maps. 

![](/README_gif/toggle_providers.gif)

They can also isolate the Google Map markers to only show the providers they're 
interested in. 

![](/README_gif/indiv_provider.gif)

## <a name=future-features></a>Future Features
* Expand insurance plans to include Dental and Vision plans
* Incorporate an insurance plan filtering system to improve user experience
* Allow users to search for all health insurance plans that their current provider
accepts
