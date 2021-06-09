import pandas as pd
from sever import cross_origin
from sever import app, events_rds, orgs_rds
@app.route("/events/<string:user_id>/<string:item_id>")
@cross_origin()
def events_recommend(user_id,item_id):
    df=pd.read_csv("database/events_clicking.csv")
    a=df[df["user_id"]==user_id] 
    a=a[a["item_id"]==item_id]
    if a.index.size==0:
    #If user first time click to item then create a new row 
      df.loc[len(df.index)]=[user_id,item_id,1]
    else:
    #If user already clicked then increase the amount of click by 1 
      df.at[a.index[0], 'Clicking'] =a["Clicking"]+1
    #Save data to clicking.csv
    df.to_csv("database/events_clicking.csv",index=False) 

    clicking=pd.read_csv("database/events_clicking.csv", encoding="latin-1")
    category=pd.read_csv("database/events_category.csv", encoding="latin-1")
    #refresh lại data
    events_rds.refresh_data(clicking, category)
    dict={
      'list_of_recommend':events_rds.recommend(user_id,item_id)
    }
   
    return dict

@app.route("/events/<string:item_id>")
@cross_origin()
def guest_events_recommend(item_id):
    df=pd.read_csv("database/events_clicking.csv")
    a=df[df["user_id"]=="anonymous"] 
    a=a[a["item_id"]==item_id]
    if a.index.size==0:
    #If user first time click to item then create a new row 
      df.loc[len(df.index)]=["anonymous",item_id,1]
    else:
    #If user already clicked then increase the amount of click by 1 
      df.at[a.index[0], 'Clicking'] =a["Clicking"]+1
    #Save data to clicking.csv
    df.to_csv("database/events_clicking.csv",index=False)
    dict={
      "list_of_recommend": events_rds.hottest(item_id)
    }
    return dict 



@app.route("/orgs/<string:user_id>/<string:item_id>")
@cross_origin()
def orgs_recommend(user_id,item_id):
    df=pd.read_csv("database/orgs_clicking.csv")
    a=df[df["user_id"]==user_id] 
    a=a[a["item_id"]==item_id]
    if a.index.size==0:
    #If user first time click to item then create a new row 
      df.loc[len(df.index)]=[user_id,item_id,1]
    else:
    #If user already clicked then increase the amount of click by 1 
      df.at[a.index[0], 'Clicking'] =a["Clicking"]+1
    #Save data to clicking.csv
    df.to_csv("database/orgs_clicking.csv",index=False) 

    clicking=pd.read_csv("database/orgs_clicking.csv", encoding="latin-1")
    category=pd.read_csv("database/orgs_category.csv", encoding="latin-1")
    #refresh lại data
    orgs_rds.refresh_data(clicking, category)
    dict={
      'list_of_recommend':orgs_rds.recommend(user_id,item_id)
    }
    
    return dict


@app.route("/orgs/<string:item_id>")
@cross_origin()
def guest_orgs_recommend(item_id):
    df=pd.read_csv("database/orgs_clicking.csv")
    a=df[df["user_id"]=="anonymous"] 
    a=a[a["item_id"]==item_id]
    if a.index.size==0:
    #If user first time click to item then create a new row 
      df.loc[len(df.index)]=["anonymous",item_id,1]
    else:
    #If user already clicked then increase the amount of click by 1 
      df.at[a.index[0], 'Clicking'] =a["Clicking"]+1
    dict={
      "list_of_recommend": orgs_rds.hottest(item_id)
    }
    return dict