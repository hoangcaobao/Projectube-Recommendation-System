from sever import app, events_rds, orgs_rds
from sever import cross_origin
@app.route('/welcome/<string:user_id>')
@cross_origin()
def welcome(user_id):
  return {**events_rds.welcome_recommend(user_id),**orgs_rds.welcome_recommend(user_id)}

@app.route('/welcome')
@cross_origin()
def guest_welcome():
  return {**events_rds.welcome(),**orgs_rds.welcome()}
