from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd


import mars_scraper

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scraperDB")

@app.route('/')
def index():
    
    mars_mongo = mongo.db.Mission_To_Mars.find_one()
    return render_template("index.html", mars=mars_mongo, mars_facts=mars_mongo['Mars_Facts'][0])

@app.route('/scrape')
def scrape():
    mars_data = mars_scraper.scrape()
    mongo.db.Mission_To_Mars.drop()

    
    mongo.db.Mission_To_Mars.insert_one(mars_data)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
