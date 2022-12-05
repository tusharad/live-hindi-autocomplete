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
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <title>Hindi AutoComplete</title>
</head>
<body>
<div class="container">
    <h1 class="text-center text-primary mt-3 mb-3">Hindi AutoComplete using SQLite3</h1>
<button class="btn btn-primary" onclick=saveTextAsFile(input.value)>Download</button>
        <textarea rows="4" style="border:solid black 1px" id="input" name="query" class="form-control form-control-lg">
         
        </textarea>

       <span id="suggestions2"></span>
        <span id="suggestions"></span>
 </div>
 <script type="text/javascript">



   function getCaretPosition(ctrl) {
    var start, end;
    if (ctrl.setSelectionRange) {
        start = ctrl.selectionStart;
        end = ctrl.selectionEnd;
    } else if (document.selection && document.selection.createRange) {
        var range = document.selection.createRange();
        start = 0 - range.duplicate().moveStart('character', -100000);
        end = start + range.text.length;
    }
    return {
        start: start,
        end: end
    }
}

$("textarea").on("click keyup", function () {
    var caret = getCaretPosition(this);
    var endPos = this.value.indexOf(' ',caret.end);
    if (endPos ==-1) endPos = this.value.length;
    var result = /\S+$/.exec(this.value.slice(0, endPos));
    var lastWord = result ? result[0] : null;
    if (lastWord) lastWord = lastWord.replace(/['";:,.\/?\\-]$/, ''); // remove punctuation
   console.log(lastWord)
   var word = lastWord;
if(word){
            storeClientCache(word);
            getData(word);
       }     

});


    function getData(query) {
		fetch('/search?query=' + query + '').then(function (response) {
            var stringObj = localStorage['wordFreq'] || '[]';
            freqMap = JSON.parse(stringObj);

            var html = '<ul class="list-group" >';
			for(var cnt = 0;cnt < freqMap.length;cnt++){
                if (freqMap[cnt].substr(0, query.length) == query && query != ""){
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
        console.log("storing");
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

function saveTextAsFile(textToWrite, fileNameToSaveAs)
    {
    	var textFileAsBlob = new Blob([textToWrite], {type:'text/plain'}); 
    	var downloadLink = document.createElement("a");
   var currentdate = new Date(); 
var datetime = "Last Sync: " + currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " @ "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds() + ".txt";

    	downloadLink.download = datetime;
    	downloadLink.innerHTML = "Download File";
    	if (window.webkitURL != null)
    	{
    		// Chrome allows the link to be clicked
    		// without actually adding it to the DOM.
    		downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
    	}
    	else
    	{
    		// Firefox requires the link to be added to the DOM
    		// before it can be clicked.
    		downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
    		downloadLink.onclick = destroyClickedElement;
    		downloadLink.style.display = "none";
    		document.body.appendChild(downloadLink);
    	}
    
    	downloadLink.click();
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
