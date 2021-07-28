import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import random

class CF_events():
  #k is the number of users using to recommend for current user
  #clicking is a table contain the amount of clicking of user_id for item_id
  #category is the table cotain category of item_id
  #number_of_recommend is a number of item recommend to user
  def __init__(self,events_clicking,events_category,k,number_of_recommend):
    self.k=k
    self.clicking=events_clicking
    self.recommended_items_final=[]
    self.category=events_category
    self.number_of_recommend=number_of_recommend
   
  
  #clean_data has index of each row (item)
  #clean_data1 is numpy type of clean_data
  #clean_data2 do not have index of each row(item) 
  #clean_data3 is the total amount of clicking of each item 
  # sim is the table compare the cosine similarity each user
  #csr_data use to decrease sparse data
  def preprocessing_data(self):
    try:
      self.clean_data=self.clicking.pivot(index="item_id",columns="user_id",values="Clicking")
      self.clean_data3=self.clean_data.sum(axis=1)
      #standarization data
      
      self.clean_data=(self.clean_data-self.clean_data.mean()+(1e-8))/(self.clean_data.std()+(1e-8))
    
      self.clean_data.fillna(0,inplace=True)
      self.clean_data1=np.array(self.clean_data)
      self.clean_data2=self.clean_data.copy()
      csr_data=csr_matrix(self.clean_data)
      self.clean_data.reset_index(inplace=True)
      self.sim=cosine_similarity(csr_data.T,csr_data.T)

      self.delete()
    except:
      pass
    
    
  def pred(self,user_id,item_id):
    #get index of other user clicked to item id, current user, and item
    users_clicked_item_id=self.clicking[self.clicking["item_id"]==item_id]["user_id"]
    users_clicked_item_index=[self.clean_data2.columns.get_loc(i) for i in users_clicked_item_id]
    user_index=self.clean_data2.columns.get_loc(user_id)
    item_index=self.clean_data[self.clean_data["item_id"]==item_id].index[0]
    
    #check whether user click item or not, if already click do not recommend
    if self.clean_data1[item_index,user_index]!=0:
      return False
    
    #get sim of current user and other users clicked to item
    #get k users has highest sim to current user
    sim_user=self.sim[user_index,users_clicked_item_index]
    most_similar_index=np.argsort(sim_user)[-self.k:]
    most_similar_user_index=[]
    for i in most_similar_index:
      most_similar_user_index.append(users_clicked_item_index[i])

    #the function to predict how much user will click to item
    largest_sim=sim_user[most_similar_index]
    click_value=self.clean_data1[item_index,most_similar_user_index]
    pred=(click_value*largest_sim).sum()/(np.abs(largest_sim).sum()+1e-8)
    return pred
  
  def recommend(self,user_id,item_id):
    recommended_items_final=[]
    recommended_items_CF=[]
    
    #Sort item with pred score
    for item in self.clean_data2.index:
      #Check whether user clicked item or not
      if self.pred(user_id,item)==False:
        continue
      recommended_items_CF.append((item,self.pred(user_id,item)))
    recommended_items_CF.sort(key=lambda x: x[1])
  
    #Choose half item has highest pred score
    recommended_items_CF=recommended_items_CF[-int(self.number_of_recommend/2):]
    
    for item in recommended_items_CF:
      recommended_items_final.append(item[0])
    
    #Sort items with number of category that are the same with current item and total amount of click
    if len(self.category[self.category["item_id"]==item_id])==0:
      item_category=[]
    else:  
      item_category=self.category[self.category["item_id"]==item_id].to_numpy()[0][1:]
    
    #Remove nan category 
    nan_position=[]
    for i in range(len(item_category)-1,-1,-1):
        if item_category[i]!=item_category[i]:
            nan_position.append(i)
    for i in nan_position:
        item_category=np.delete(item_category,i)
    items_score=[]
    for item in self.category['item_id']:
      #check whether item has already in recommend list
      if item==item_id or item in recommended_items_final:
        continue
      category_score=0
      if len(self.category[self.category['item_id']==item])==0:
        continue
      for i in self.category[self.category["item_id"]==item].to_numpy()[0][1:]:
        #plus 1 to score if have the same category
        if i in item_category:
          category_score+=1
      try:
        clicking_score=self.clean_data3.loc[item]
      except:
        clicking_score=0
      items_score.append((item, category_score, clicking_score))
        
    items_score.sort(key=lambda x: (x[1], x[2]),reverse=True)
    
   
    #choose items until recommended_items_list full 
    for i in range(len(items_score)):
      if len(recommended_items_final)==self.number_of_recommend-2:
        items_score=items_score[i:]
        random.shuffle(items_score)
        break
      recommended_items_final.append(items_score[i][0])
    for i in range(len(items_score)):
      if len(recommended_items_final)==self.number_of_recommend:
        break
      recommended_items_final.append(items_score[i][0])
    return recommended_items_final

  #update data
  def refresh_data(self,events_clicking,events_category):
    self.clicking=events_clicking
    self.category=events_category
    self.preprocessing_data()

  def hottest(self,item_id):
    if len(self.category[self.category["item_id"]==item_id])==0:
      item_category=[]
    else:  
      item_category=self.category[self.category["item_id"]==item_id].to_numpy()[0][1:]
    
    #Remove nan category 
    nan_position=[]
    for i in range(len(item_category)):
        if item_category[i]!=item_category[i]:
            nan_position.append(i)
    for i in nan_position:
        item_category=np.delete(item_category,i)
    items_score=[]
    for item in self.category['item_id']:
      #check whether item has already in recommend list
      if item==item_id :
        continue
      category_score=0
      if len(self.category[self.category['item_id']==item])==0:
        continue
      for i in self.category[self.category["item_id"]==item].to_numpy()[0][1:]:
        #plus 1 to score if have the same category
        if i in item_category:
          category_score+=1
      try:
        clicking_score=self.clean_data3.loc[item]
      except:
        clicking_score=0
      items_score.append((item, category_score, clicking_score))
        
    items_score.sort(key=lambda x: (x[1], x[2]),reverse=True)
    recommend_list=[]
    for i in range(len(items_score)):
      recommend_list.append(items_score[i][0])
    
    return recommend_list
    
  def welcome_recommend(self,user_id):
    dic={
      'hottest_events':[],
      'care_events':[],
    }
    try:
      recommended_items_CF=[]
      #Sort item with pred score
      for item in self.clean_data2.index:
        #Check whether user clicked item or not
        if self.pred(user_id,item)==False:
          continue
        recommended_items_CF.append((item,self.pred(user_id,item)))
      recommended_items_CF.sort(key=lambda x: x[1])
    
      for i in range(len(recommended_items_CF)):
        recommended_items_CF[i]=recommended_items_CF[i][0]
      
      #Choose 10 item with highest pred score 
      if len(recommended_items_CF)>10:
        recommended_items_CF=recommended_items_CF[-10:]
      dic['care_events']=recommended_items_CF
    except:
      pass
    #Sort item with highest amount of click 
    self.clean_data3=self.clean_data3.sort_values(ascending=False)
    recommended_items_hottest=[]
    count=0
    #Choose 10 hottest item
    items_score=[]
    for item in self.category['item_id']:
      try:
        clicking_score=self.clean_data3.loc[item]
      except:
        clicking_score=0
      items_score.append((item,  clicking_score))
        
    items_score.sort(key=lambda x: (x[1]),reverse=True)
    for i in items_score:
      if count==100:
        break
      recommended_items_hottest.append(i[0])
      count+=1
    dic['hottest_events']=recommended_items_hottest
    return dic
  def welcome(self):
    items_score=[]
    self.clean_data3=self.clean_data3.sort_values(ascending=False)
    recommended_items_hottest=[]
    count=0
    dic={
     'hottest_events':[],
    }
    for item in self.category['item_id']:
      try:
        clicking_score=self.clean_data3.loc[item]
      except:
        clicking_score=0
      items_score.append((item,  clicking_score))
        
    items_score.sort(key=lambda x: (x[1]),reverse=True)
    for i in items_score:
      if count==100:
        break
      recommended_items_hottest.append(i[0])
      count+=1
    dic['hottest_events']=recommended_items_hottest
    return dic
  
  def delete(self):
    #delete an event in clicking due to the removal
    total_item= self.category["item_id"]
    clicking_item= self.clicking["item_id"]
    contain=[]
    for i in clicking_item:
      check=False
      for j in total_item:
        if(i==j):
          check=True
          break
      if(check==False):
        contain.append(i)
    for i in contain:
      self.clicking=self.clicking[self.clicking["item_id"]!=i]
    self.clicking.to_csv('database/events_clicking.csv',index=False)
