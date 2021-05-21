import requests
from sever import app
from run import link
import pandas as pd
#function to get graphql 
def run_query(query):
  global link
  request = requests.post(link, json={'query': query})
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
@app.route("/update")
def update():
    #query sql api
    events_query = """
    {
    events{
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
    orgs{
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

    #create pandas framework from dic then save it to category
    df=pd.DataFrame(data=dic)
    df.to_csv('database/orgs_category.csv',index=False)
    return "UPDATED"
