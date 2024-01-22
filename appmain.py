from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)


def convertdata(date):
    date_string = date
    parsed_date = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
    formatted_date = parsed_date.strftime("%d-%m-%Y")
    return formatted_date


def is_date_between(target_date_str, start_date_str, end_date_str):
    target_date = datetime.strptime(target_date_str, '%d-%m-%Y')
    start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
    end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
    return start_date <= target_date <= end_date

def is_between(no,nofrom,noto):
    x=(no>=nofrom and no<=noto)
    print(no,nofrom,noto)
    return x

def contain(str,searchstr):
    print(searchstr)
    main_str_lower = str.lower()
    search_str_lower = searchstr.lower()
    x=search_str_lower in main_str_lower
    print(search_str_lower)
    return x

@app.route('/search', methods=['GET'])
def search_comments():
    search_author = request.args.get('search_author', default="", type=str)
    at_from = request.args.get('at_from', default="01-01-0001", type=str)
    at_to = request.args.get('at_to', default="01-01-9999", type=str)
    like_from = request.args.get('like_from', default=0, type=int)
    like_to = request.args.get('like_to', default=10000000000, type=int)
    reply_from = request.args.get('reply_from', default=0, type=int)
    reply_to = request.args.get('reply_to', default=10000000000, type=int)
    search_text = request.args.get('seach_text', default="", type=str)  
    response = requests.get('https://app.ylytic.com/ylytic/test')
    print(search_text)
    if response.status_code == 200:
        data = response.json()
        mydict = {"comments": []}
        for i in range(len(data["comments"])):
            print()
            temp=convertdata(data["comments"][i]["at"])
            if(contain(data["comments"][i]["author"],search_author) and 
               is_date_between(temp,at_from,at_to) and 
               is_between(data["comments"][i]["like"],like_from,like_to) and
               is_between(data["comments"][i]["reply"],reply_from,reply_to) and 
               contain(data["comments"][i]["text"],search_text)  
            ):
                mydict["comments"].append(data["comments"][i])
        return jsonify(mydict)
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500


if __name__ == '__main__':
    app.run(debug=True)
