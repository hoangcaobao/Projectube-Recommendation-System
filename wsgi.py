from sever import app
from sever.update import update, set_interval

if __name__=="__main__":
  set_interval(update,5)
  app.run(debug=True)
    