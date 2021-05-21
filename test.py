import requests
link ="http://beta.projectube.org/api/gql"
def run_query(query):
  global link
  request = requests.post(link, json={'query': query})
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

query="""

{
   users {
        id
        
    }
}
"""
events = run_query(query) 
events=events['data']['users']
print(events)