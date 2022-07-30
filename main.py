from flask import Flask
from flask import render_template

import requests
from bs4 import BeautifulSoup

URL = "https://www.imdb.com/title/tt11198330/fullcredits"

app = Flask(__name__)

DEBUG=False
if not DEBUG:
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html.parser")
else:
    f = open("site.html")
    soup = BeautifulSoup(f.read(), "html.parser")

table = soup.find("table", {"class" : "cast_list"})

characters = table.find_all("td", {"class":"character"})
character_names = [c.a.text for c in characters]

photo_td = table.find_all("td", {"class":"primary_photo"})
real_names = [p.a.img.attrs["alt"] for p in photo_td]

targaryens = {}
for c, r in zip(character_names, real_names):
    if "Targaryen" in c:
        targaryens[c] = r
    
@app.route("/")
def index():
    return render_template("index.html", targaryens=targaryens)
