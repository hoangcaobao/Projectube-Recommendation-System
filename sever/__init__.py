from flask import Flask
from collaborative_filtering.events import CF_events
from collaborative_filtering.orgs import CF_orgs
import pandas as pd

app=Flask(__name__)
link="http://beta.projectube.org/api/gql"
events_clicking=pd.read_csv("database/events_clicking.csv", encoding="latin-1")
events_category=pd.read_csv("database/events_category.csv", encoding="latin-1")
events_rds=CF_events(events_clicking,events_category,2,8)
events_rds.preprocessing_data()   
orgs_clicking=pd.read_csv("database/orgs_clicking.csv", encoding="latin-1")
orgs_category=pd.read_csv("database/orgs_category.csv", encoding="latin-1")
orgs_rds=CF_orgs(orgs_clicking,orgs_category,2,8)
orgs_rds.preprocessing_data()   
from sever import index
from sever import welcome
from sever import recommend