from flask import Flask, request, jsonify
import requests
import urllib
from bs4 import BeautifulSoup
import json
from gtts import gTTS
import IPython.display as ipd
from IPython.core.display import HTML


def getWeather(city) :    
    url = "https://search.naver.com/search.naver?query="
    url = url + urllib.parse.quote_plus(city + "날씨")
    print(url)
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    temp = bs.select('span.todaytemp')    
    desc = bs.select('p.cast_txt')    
    return  {"temp":temp[0].text, "desc":desc[0].text}

def getwcl(server, name) :    
    url = "https://www.warcraftlogs.com/character/kr/"
    url = url + urllib.parse.quote_plus(server) + "/" + urllib.parse.quote_plus(name)    
    return url

def gettier(name) :    
    url = "https://www.op.gg/summoner/userName="
    url = url + urllib.parse.quote_plus(name) 
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    tier = bs.select('div.TierRank')    
    return {"tier":tier[0].text}
    

def getQuery(word):
    url = "https://search.naver.com/search.naver?where=kdic&query="
    url = url + urllib.parse.quote_plus(word)
    print(url)
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    output = bs.select('p.txt_box')
    return [node.text for node in output]



app = Flask(__name__)
cnt = 0 #전역변수 global 필요

@app.route('/')
def home():
    html = """
    <h1>Hi</h1>
    <img src=/static/chloe.png><br>
    <iframe
    allow="microphone;"
    width="350"
    height="430"
    src="https://console.dialogflow.com/api-client/demo/embedded/beek06">
</iframe>
"""
    return html

@app.route('/counter')
def counter():
    global cnt
    visitTotal = ""
    cnt += 1
    for i in str(cnt):
        visitTotal += f"<img src=/static/{i}.png width=40>" 
    visitTotal += "명이 방문하였습니다."
    
    return visitTotal

@app.route('/weather', methods=["POST", "GET"])
def weather():
    if request.method == "GET":
        req = request.args 
    else:
        req = request.form
        
    # city = request.form.get("city", "default") 입력값이 없을 시 default 사용 
    
    #req = requst.arg if request.method == "GET" else request.form
    
    city = req.get("city")
    info = getWeather(city)
    
    return jsonify(info)
    

# @app.route('/')
# def home():
#     name = request.args.get("name")
#     item = request.args.get("item")
#     return "hello" + name + item

# @app.route('/weather')
# def weather():
#     city = request.args.get("city")
#     info = getWeather(city)
#     return jsonify(info)

@app.route('/dialogflow', methods=['POST', 'GET'])
def dialoglfow():
    req = request.get_json(force=True) #강제로 json화
    print(json.dumps(req, indent=4, ensure_ascii=False))
    
    answer = req['queryResult']['fulfillmentText']
    intentName = req['queryResult']['intent']['displayName']
    
    if intentName == 'query':
        word = req['queryResult']['parameters']['any']
        text = getQuery(word)[0]
        res = {'fulfillmentText': text}
        
    elif intentName == 'weather':
        date = req['queryResult']['parameters']['date-time']
        geo_city = req['queryResult']['parameters']['geo-city1']
        info = getWeather(geo_city)
        text = f"{geo_city} 날씨 정보 : {info['temp']} /  {info['desc']}"
        res = {'fulfillmentText': text}
        
    elif intentName == 'wcl finder - wcl - end':
        server = req['queryResult']['parameters']['serverName']
        name = req['queryResult']['parameters']['any']
        info = getwcl(server, name)
        res = {'fulfillmentText': f'{info}'}
        
    elif intentName == 'lol - stat':
        name = req['queryResult']['parameters']['any']
        info = gettier(name)
        text = info['tier']
        res = {'fulfillmentText': f'{text}'}
            
    else:
        res = {'fulfillmentText': answer}
        
    
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

    
