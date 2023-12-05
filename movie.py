import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

import requests
from bs4 import BeautifulSoup
url = "http://www.atmovies.com.tw/movie/next/"
Data = requests.get(url)
Data.encoding = "utf-8"
sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select(".filmListAllX li")
lastUpdate = sp.find("div", class_="smaller09").text[5:]

for x in result:
	picture = x.find("img").get("src").replace(" ","")
	title = x.find("img").get("alt")
	movie_id = x.find("div", class_="filmtitle").find("a").get("href").replace("/", "").replace("movie", "")
	hyperlink = "http://www.atmovies.com.tw" + x.find("a").get("href")
	show = x.find(class_ ="runtime").text.replace("上映日期：", "")
	show = show.replace("片長：", "")
	show = show.replace("分", "")
	showDate = show[0:10]
	showLength = show[13:]

	doc = {
		"title": title,
		"picture": picture,
		"hyperlink": hyperlink,
		"showDate": showDate,
		"showLength": showLength,
		"lastUpdate": lastUpdate
	}
	doc_ref = db.collection("電影").document(movie_id)
	doc_ref.set(doc)
