from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin

from mongoDBOperations import MongoDBManagement  # User define classes
from WikipediaScrapping import WikipediaScrapper   # User define classes

app = Flask(__name__)

db_object = MongoDBManagement(userid="sumegh", password="sumegh12345")
database_name = "WikiScrapper"
free_status = True

@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    return render_template('Input.html')

@app.route('/getData', methods=['POST', 'GET'])
@cross_origin()
def getData():
    try:
        if request.method == 'POST':
            global free_status    # To maintain the internal server issue on heroku
            if free_status != True:
                return "This website is executing some process. Kindly try after some time..."
            else:
                free_status = True
            searchString = request.form['content'].replace(" ", "_")  # obtaining the search string entered in the form
            if not db_object.isCollectionPresent(db_name=database_name, collection_name=searchString):
                wiki_object = WikipediaScrapper()
                wiki_object.openUrl(url='https://www.wikipedia.org/')
                wiki_object.getTheSearchPage(searchString=searchString)
                response = wiki_object.getResultDict(searchString=searchString)
                db_object.insertOneRecord(record=response, db_name=database_name, collection_name=searchString)

            result = db_object.getRecordsOnQuery(db_name=database_name, collection_name=searchString,
                                                            query={"Topic": searchString})

            result[0].pop('_id')
            result1 = db_object.getDataFrameOfCollection(db_name=database_name, collection_name=searchString,
                                                         query={"Topic": searchString})
            result1.to_csv("Output/Scrapping_Data.csv")
            return render_template('results.html', data={"result":result[0]})

    except Exception as e:
        raise Exception(f"(getData): Something went wrong on app.py \n"+str(e))

if __name__ == "__main__":
    app.run()  # running the app on the local machine on port 8000