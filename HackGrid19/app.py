# app setup
from flask import *
from flask_pymongo import PyMongo
app = Flask(__name__)

# importing libraries
import scripts.text_extract as extract
import scripts.synonyms as synonyms
import scripts.getlang as language


token_lists = []

app.config['MONGO_DBNAME'] = 'try_app_users'
app.config['MONGO_URI'] = 'mongodb://kunal:sahni1@ds163905.mlab.com:63905/domain_data'

mongo  = PyMongo(app)


# routes
@app.route("/",methods = ['GET','POST'])
def welcome_search():
    # clear on start
    global token_lists
    token_lists.clear()

    if request.method == "GET":
        return render_template("main.html")
    elif request.method == "POST":
        #global token_lists
        company = request.form['company']
        associated_tags = request.form['tags']
        description = request.form['description']
        location = request.form['location']

        labels = [company , associated_tags ]
        for label in labels :
            token_lists += labels + extract.extract_tag(label) + synonyms.get_synonyms(label)

        #print(token_lists)
        token_lists = list(set(token_lists))

        token_lists = extract.make_pairs(token_lists)

        token_lists = list(set(token_lists))

        


        return redirect(url_for("search_results"))


@app.route("/search",methods = ["GET","POST"])
def search_results():
    if request.method == "GET":
        global token_lists
        return render_template("query.html",queries = token_lists)








if __name__ == "__main__":
    app.run(debug = True)
