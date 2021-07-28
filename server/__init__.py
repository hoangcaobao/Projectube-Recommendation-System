from flask import Flask
from flask_cors import CORS, cross_origin
from collaborative_filtering.events import CF_events
from collaborative_filtering.orgs import CF_orgs
import pandas as pd
import os
app=Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
link=os.environ.get("GRAPHQL")
events_clicking=pd.read_csv("database/events_clicking.csv", encoding="latin-1")
events_category=pd.read_csv("database/events_category.csv", encoding="latin-1")
events_rds=CF_events(events_clicking,events_category,3,10)
events_rds.preprocessing_data()   
orgs_clicking=pd.read_csv("database/orgs_clicking.csv", encoding="latin-1")
orgs_category=pd.read_csv("database/orgs_category.csv", encoding="latin-1")
orgs_rds=CF_orgs(orgs_clicking,orgs_category,3,10)
orgs_rds.preprocessing_data()   
from server import index
from server import welcome
from server import recommend
