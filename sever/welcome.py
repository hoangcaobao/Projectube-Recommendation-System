from sever import app, events_rds, orgs_rds
@app.route('/welcome/<string:user_id>')
def welcome(user_id):
  return {**events_rds.welcome_recommend(user_id),**orgs_rds.welcome_recommend(user_id)}
