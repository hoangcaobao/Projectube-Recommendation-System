from sever import app
from sever import cross_origin
@app.route('/')
@cross_origin()
def index():
  return 'hello'