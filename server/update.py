import requests
from server import link
import pandas as pd
import threading
from server import events_rds, orgs_rds
from collaborative_filtering.events import CF_events
from collaborative_filtering.orgs import CF_orgs
import time
#function to get graphql

def run_query(query):
  global link
  request = requests.post(link, json={'query': query})
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

#setInterval
def set_interval(func, sec):
    def func_wrapper():
        time.sleep(5)
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
   

def update():
    #query sql api
    events_query = """
    {
    events(limit: 0){
        id
        name
        categories
    }
    }
    """
    events = run_query(events_query) 
    events=events['data']['events']
    orgs_query = """
    {
    orgs(limit:0){
        id
        name
        categories
    }
    }
    """
    orgs = run_query(orgs_query) 
    orgs=orgs['data']['orgs']

    #create a dic contain id and category
    dic={'item_id':[],
        'Category_1':[],
        'Category_2':[],
        'Category_3':[],
    }
    for event in events:
        categories=event['categories']
        dic['item_id'].append(event['id'])
        if len(event['categories'])==1:
            dic['Category_1'].append(categories[0])
            dic['Category_2'].append(None)
            dic['Category_3'].append(None)
        elif len(event['categories'])==2:
            dic['Category_1'].append(categories[0])
            dic['Category_2'].append(categories[1])
            dic['Category_3'].append(None)
        else:
            dic['Category_1'].append(categories[0])
            dic['Category_2'].append(categories[1])
            dic['Category_3'].append(categories[2])
    df=pd.DataFrame(data=dic)
    df.to_csv('database/events_category.csv',index=False)
    dic={'item_id':[],
        'Category_1':[],
        'Category_2':[],
        'Category_3':[],
    }
    for org in orgs:
        categories=org['categories']
        dic['item_id'].append(org['id'])
       
        if len(org['categories'])==1:
            dic['Category_1'].append(categories[0])
            dic['Category_2'].append(None)
            dic['Category_3'].append(None)
        elif len(org['categories'])==2:
            dic['Category_1'].append(categories[0])
            dic['Category_2'].append(categories[1])
            dic['Category_3'].append(None)
        else:
            dic['Category_1'].append(categories[0])
            dic['Category_2'].append(categories[1])
            dic['Category_3'].append(categories[2])
       

    #create pandas framework from dic then save it to category
    df=pd.DataFrame(data=dic)
    df.to_csv('database/orgs_category.csv',index=False)

    #reset
    events_clicking=pd.read_csv("database/events_clicking.csv", encoding="latin-1")
    events_category=pd.read_csv("database/events_category.csv", encoding="latin-1")
    events_rds=CF_events(events_clicking,events_category,3,10)
    events_rds.preprocessing_data()   
    orgs_clicking=pd.read_csv("database/orgs_clicking.csv", encoding="latin-1")
    orgs_category=pd.read_csv("database/orgs_category.csv", encoding="latin-1")
    orgs_rds=CF_orgs(orgs_clicking,orgs_category,3,10)
    orgs_rds.preprocessing_data()  

