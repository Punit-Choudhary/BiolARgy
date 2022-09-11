import os

from dotenv import load_dotenv
from flask import Flask, request, url_for
from flask_pymongo import PyMongo

load_dotenv()

app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

@app.route('/')
def index():
    return """
        <center><h2>Super Secret Stuff 🤫💀</h2></center>
        <form method="POST" action="/submit" enctype="multipart/form-data">
            <label for='id'>ID</label>
            <input type='text' name='id' id='id'><br><br>

            <label for='name'>Name</label>
            <input type='text' name='name' id='name'><br><br>

            <label for='description'>Description</label>
            <input type='text' name='description' id='description'><br><br>

            <label for='para1'>Para1</label>
            <input type='text' name='para1' id='para1'><br><br>

            <label for='para2'>Para2</label>
            <input type='text' name='para2' id='para2'><br><br>

            <label for='image'>Image</label>
            <input type='file' name='image' id='image'><br>

            <label for='qr'>QR</label>
            <input type='file' name='qr' id='qr'><br>

            <input type="submit">
    """


@app.route('/submit', methods=['POST'])
def submit():
    _id = request.form.get('id')
    name = request.form.get('name')
    description = request.form.get('description')
    para1 = request.form.get('para1')
    para2 = request.form.get('para2')
    
    image = request.files['image']
    qr = request.files['qr']
    if _id and image:
        # saving images
        mongo.save_file(_id + '_image', image)
        mongo.save_file(_id, qr)

        mongo.db.content.insert_one({
            '_id': _id,
            'name': name,
            'description': description,
            'para1': para1,
            'para2': para2
        })
    
        return """
        <center><h1>GoodWork 😎👍</h1></center><br>
        <a href="/">
            <button>Upload More</button>
        </a>
        """
    else:
        return """
        <center><h1>📸 Don't Do it Again</h1></center><br>
        <a href="/">
            <button>Go Back</button>
        </a>
        """

@app.route('/refresh', methods=['POST'])
def refresh():
    return "repl.deploy" + str(request.json)

if __name__ == "__main__":
    app.run(debug=True)
