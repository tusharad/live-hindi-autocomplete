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

    cursorObj.execute(f"SELECT * FROM ONE_WORD_FREQ WHERE word like \'{query}%\' order by count desc limit 4")
    rows2 = cursorObj.fetchall()

    cursorObj.execute(f"SELECT * FROM TWO_WORD_FREQ WHERE word like \'{query}%\' order by count desc limit 4")
    rows3 = cursorObj.fetchall()

    return Response(json=rows2+rows3)

def home_app(response):
    body = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>Hindi AutoComplete</title>
</head>
<body>
<div class="container">
    <h1 class="text-center text-primary mt-3 mb-3">Hindi AutoComplete using SQLite3</h1>
    <button  type="button" class="btn btn-primary" href="" id="a">Download</button>
    <button type="button" class="btn btn-warning" onclick="download()">Save</button>
        <textarea rows="4" style="border:solid black 1px" id="input" name="query" class="form-control form-control-lg">
         
        </textarea>

       <span id="suggestions2"></span>
        <span id="suggestions"></span>
 </div>
 <script type="text/javascript">
    const search_area = document.querySelector('#input')
    search_area.addEventListener('input',function handleChange(e){
        data = e.target.value;
         if(data[data.length - 1] == " "){
            storeClientCache(word);
            getData(word);
            }else{
                word = data.split(" ").pop().trim();
                getData(word);
            }
    });

    function getData(query) {
		fetch('/search?query=' + query + '').then(function (response) {
            var stringObj = localStorage['wordFreq'] || '[]';
            freqMap = JSON.parse(stringObj);

            var html = '<ul class="list-group" >';
			for(var cnt = 0;cnt < freqMap.length;cnt++){
                if (freqMap[cnt].substr(0, word.length) == word && word != ""){
                    console.log("from client console");
					var regular_expression = new RegExp('(' + query + ')', 'gi');
					html += '<a href="#" style="color:red" class="list-group-item list-group-item-action" onclick="get_text(this)">' + freqMap[cnt].replace(regular_expression, '<span class="text-primary ">$1</span>') + '</a>';
				}
            }
			html += '</ul>';
			document.getElementById('suggestions2').innerHTML = html;

            return response.json();
		}).then(function (responseData) {
			var html = '<ul class="list-group">';
			for (var count = 0; count < responseData.length; count++) {
					var regular_expression = new RegExp('(' + query + ')', 'gi');
					html += '<a href="#" class="list-group-item list-group-item-action" onclick="get_text(this)">' + responseData[count][0].replace(regular_expression, '<span class="text-primary ">$1</span>') + '</a>';
				}
			html += '</ul>';
			document.getElementById('suggestions').innerHTML = html;
		});
	}

    function storeClientCache(query) {
            var stringObj = localStorage['wordFreq'] || '[]';
            var freqMap = { arr: [] };
            if (stringObj) {
                freqMap = JSON.parse(stringObj);
                if(!freqMap.includes(query)){
                    freqMap.push(query);
                }
            }
            localStorage['wordFreq'] = JSON.stringify(freqMap)
        }

    function get_text(event) {
		var text = event.textContent;
		var str = document.getElementById('input').value;
		var lastIndex = str.lastIndexOf(" ");
		str = str.substring(0, lastIndex) + " ";
		document.getElementById('input').value = str + text + " ";
		document.getElementById('suggestions').innerHTML = '';
		document.getElementById('input').focus();
	}

    function download() {
  var a = document.getElementById("a");
  const content = document.getElementById('input').value;
  var file = new Blob([content], {type: 'txt'});
  a.href = URL.createObjectURL(file);
  const d = new Date();
  a.download = d;
}
</script>

</body>
</html>    """
    return Response(body)

app_paths = {
    '/':home_app,
    '/search':search
}

httpd = make_server('',8000,main_app)
httpd.serve_forever()