# 10 rows returned in 585ms

from wsgiref.simple_server import make_server
from webob import Response
from webob.dec import wsgify
from urllib.parse import parse_qs
from math import log

import json
import sqlite3
from sqlite3 import Error

try:
    conn = sqlite3.connect("textDB.db",uri=True)
    print("connection established!")
    cursorObj = conn.cursor()
except Error:
	print(Error)

@wsgify
def main_app(request):
    path = request.environ['PATH_INFO']
    if path in app_paths:
        return app_paths[path](request)
    return ""


def search(request):
    global conn
    
    query = request.GET['query']
    cursorObj = conn.cursor()

    cursorObj.execute(f"SELECT word FROM ONE_WORD_FREQ WHERE word like \'{query}%\' order by count desc limit 4")
    rows2 = cursorObj.fetchall()

    cursorObj.execute(f"SELECT word FROM TWO_WORD_FREQ WHERE word like \'{query}%\' order by count desc limit 4")
    rows3 = cursorObj.fetchall()

    #cursorObj.execute(f"SELECT word FROM THREE_WORD_FREQ WHERE word like \'{query}%\' order by count desc limit 4")
    #rows4 = cursorObj.fetchall()

    return Response(json=rows2+rows3)

def home_app(response):
    body =    "<h1>oops! Something went wrong!</h1>"
    with open("index.html") as f:
        body = f.read()
    return Response(body)

app_paths = {
    '/':home_app,
    '/search':search
}

httpd = make_server('',8000,main_app)
print('server is running on http://localhost:8000')
httpd.serve_forever()
