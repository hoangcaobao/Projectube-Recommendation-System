from flask import Flask
app=Flask(__name__)
from sever import index
from sever import welcome
from sever import update
from sever import recommend