# Live Hindi Autocomplete

Project members:

- Tushar Adhatrao (21111049)
- Akshay Patil (21111022)

Web-based application that gives live suggestions as you type hindi characters.

It is a semester wide project being done under the guidance of **Damodar Kulkarni (PUCSD)**

# Technology used
- Sqlite3
- Python
- Javascript (Jquery)

# Journey
Here are various milestones I reached during this project:

## Finding dataset for processing

Downloaded wikidump containing all the hindi articles from wikipedia. [here](https://dumps.wikimedia.org/hiwiki/20221220/). It was 1.7 GB xml file.


## Parsing XML file

Wrote a small tool in python, to parse XML file and get the articles, their title and link and store it into the database. Making unstructured data into structured.

## Processing on large text file

Put all that data into a single text file. Now needed to find the frequency of each word in that file.

## Performing external merge sort to find frequency of each word

Performed external merged sort on that data. Spliting the text file into smaller text files and then merging them back after sorting.

## Created the SQLite3 database containing 200K words

Once I had the words sorted. Counted the frequency of each word and inserted it into the database.

## Wrote Python web server using WSGI

Built a web server using Python WSGI (Web server gateway interface).

## Used Javascript for live sql query firing

Used to Jquery to fire query and fetch data from database as words are being typed on the text area.


## Showing result with highlighted part.

Showed fetched data in the tabular form.

## Used client side caching for personalized suggestions

Stored typed words in the browser's cache. And fetch them first next time onwards.

## Suggested words which are currently pointed by the caret/cursor

## Shortcut for word completion

User can type alt + (index of suggested word), to complete the suggestion.

## Download written text