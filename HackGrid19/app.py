# app setup
from flask import *
import pymongo
from flask_pymongo import PyMongo
app = Flask(__name__)
import json
import urllib.request
import os
# importing libraries
import scripts.text_extract as extract
import scripts.synonyms as synonyms
import scripts.getlang as language
import scripts.maps as map
import scripts.request_image as reqimage

token_lists = []
company_name = None
db_uri = 'mongodb://kunal:sahni1@ds163905.mlab.com:63905/domain_data'

app.config['MONGO_DBNAME'] = 'domain_data'
app.config['MONGO_URI'] = db_uri

client = pymongo.MongoClient(db_uri)
db = client['domain_data']

mongo  = PyMongo(app)


# routes
@app.route("/",methods = ['GET','POST'])
def welcome_search():
    if request.method == "GET":
        global token_lists
        token_lists.clear()
        return render_template("main.html")
    elif request.method == "POST":
        company = request.form['company']
        associated_tags = request.form['tags']
        description = request.form['description']
        location = request.form['location']

        global company_name
        company_name = company

        labels = [company , associated_tags ]

        for label in labels :
                token_lists += labels + extract.extract_tag(label) + synonyms.get_synonyms(label)

        #print(token_lists)
        token_lists = list(set(token_lists))

        token_lists = extract.make_pairs(token_lists)

        token_lists = list(set(token_lists))

        available = db.available
        available.insert({"company" : company ,"list":token_lists })

        print(company_name)
        return redirect(url_for("search_results"))


@app.route("/search",methods = ["GET","POST"])
def search_results():
    if request.method == "GET":

        available = db.available
        queries = dict(available.find_one({"company" : company_name}))
        #print(queries["list"])
        selective_query = []

        for name in queries["list"]:
            if company_name in name:
                selective_query.append(name)

        return render_template("query.html",queries = selective_query)

    elif request.method == "POST":

        country = request.form['country']
        city = request.form['city']
        final_domain_name = request.form['final_domain']
        #import pdb; pdb.set_trace()
        geolocs = map.get_geolocations(city,country)
        url = "https://maps.googleapis.com/maps/api/staticmap?size=400x400^&center="+str(geolocs[0])+","+str(geolocs[1])+"^&zoom=4^&path=weight:3%7Ccolor:orange%7Cenc:_fisIp~u%U}%7Ca@pytA_~b@hhCyhS~hResU%7C%7Cx@oig@rwg@amUfbjA}f[roaAynd@%7CvXxiAt{ZwdUfbjAewYrqGchH~vXkqnAria@c_o@inc@k{g@i`]o%7CF}vXaj\h`]ovs@?yi_@rcAgtO%7Cj_AyaJren@nzQrst@zuYh`]v%7CGbldEuzd@%7C%7Cx@spD%7CtrAzwP%7Cd_@yiB~vXmlWhdPez\_{Km_`@~re@ew^rcAeu_@zhyByjPrst@ttGren@aeNhoFemKrvdAuvVidPwbVr~j@or@f_z@ftHr{ZlwBrvdAmtHrmT{rOt{Zz}E%7Cc%7C@o%7CLpn~AgfRpxqBfoVz_iAocAhrVjr@rh~@jzKhjp@``NrfQpcHrb^k%7CDh_z@nwB%7Ckb@a{R%7Cyh@uyZ%7CllByuZpzw@wbd@rh~@%7C%7CFhqs@teTztrAupHhyY}t]huf@e%7CFria@o}GfezAkdW%7C}[ocMt_Neq@ren@e~Ika@pgE%7Ci%7CAfiQ%7C`l@uoJrvdAgq@fppAsjGhg`@%7ChQpg{Ai_V%7C%7Cx@mkHhyYsdP%7CxeA~gF%7C}[mv`@t_NitSfjp@c}Mhg`@sbChyYq}e@rwg@atFff}@ghN~zKybk@fl}A}cPftcAite@tmT__Lha@u~DrfQi}MhkSqyWivIumCria@ciO_tHifm@fl}A{rc@fbjAqvg@rrqAcjCf%7Ci@mqJtb^s%7C@fbjA{wDfs`BmvEfqs@umWt_Nwn^pen@qiBr`xAcvMr{Zidg@dtjDkbM%7Cd_@^&key="

        #reqimage.requests_image(url)

        #return redirect(url_for("get_maps"))
        #urllib.request.urlopen(url)
        os.system("start "+ url)
        return redirect(url_for("welcome_search"))
    #    return redirect(url_for("welcome_search"))

@app.route("/maps",methods = ["GET","POST"])
def get_maps():
    if request.method == "GET":
        return render_template("maps.html")




if __name__ == "__main__":
    app.run(debug = True)
