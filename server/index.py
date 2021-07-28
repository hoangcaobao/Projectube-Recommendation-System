from server import app
from server import cross_origin
@app.route('/')
@cross_origin()
def index():
  return 'hello'