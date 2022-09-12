import os

# from flask_pymongo import PyMongo
from flask import Flask, render_template, url_for
from dotenv import load_dotenv

import model

load_dotenv('./Database/.env')

app = Flask(__name__)

# mongodb setup
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = model.PyMongoFixed(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/img/<path:filename>')
def img(filename):
    return mongo.send_file(filename)

@app.route('/library')
def library():
    html_code = []
    content = mongo.db['content']
    for doc in content.find():
        _id = doc['_id']
        name = doc['name']
        description = doc['description']
        thumbnail = url_for('img', filename=_id + '_image')

        code = f"""
                        <div class="col-xl-6 col-md-6 col-lg-6">
                        <div class="single_delicious d-flex align-items-center">
                            <div class="thumb">
                                <img src="{thumbnail}" alt="{name}" style="height: 166px; width: 166px; padding: 20px;">
                            </div>
                            <div class="info">
                                <h3>{name}</h3>
                                <p>{description}</p>
                                <span><button onclick="location.href='{url_for('read', _id=_id)}';" class="btn">Read About {name}</button></span> 
                            </div>
                        </div>
                    </div>
        """

        html_code.append(code)
    
    return render_template('library.html', html_code=html_code)


@app.route('/read/<_id>')
def read(_id):
    content = mongo.db['content']
    doc = content.find_one({'_id': _id})
    name = doc['name']
    para1 = doc['para1']
    para2 = doc['para2']
    qr = url_for('img', filename=_id)

    return render_template('read.html', name=name, para1=para1, para2=para2, qr=qr)

if __name__ == "__main__":
    app.run(debug=True)