from flask import Flask, redirect, url_for, \
				  request, render_template, json,jsonify
from pymongo import MongoClient
import pymongo
import os
import socket
from bson import ObjectId



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


client = MongoClient('mongodb://backend:2345/dockerdemo')
db = client.blogpostDB

app = Flask(__name__)

@app.route("/")
def landing_page():
    posts = get_all_posts()
    
    return render_template('blog.html', posts=json.loads(posts))


@app.route('/add_post', methods=['POST'])
def add_post():

    new()
    return redirect(url_for('landing_page'))

@app.route('/remove_post', methods=['POST'])
def remove_post():
    delete()
    return redirect(url_for('landing_page'))


@app.route('/update_post', methods=['POST'])
def update_post():
    update()
    
    return redirect(url_for('landing_page'))


@app.route('/remove_all')
def remove_all():
    db.blogpostDB.delete_many({})

    return redirect(url_for('landing_page'))


@app.route('/swaggerjson')
def get_swagger_json():
    with open('swagger.json') as json_file:
        data = json.load(json_file)

    return jsonify(data)




## Services

@app.route("/posts", methods=['GET'])
def get_all_posts():
    
    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    for post in posts:
        print post

    return JSONEncoder().encode(posts)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'title': request.form['title'],
        'post': request.form['post']
    }
    db.blogpostDB.insert_one(item_doc)

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    return JSONEncoder().encode(posts[-1])


@app.route('/update', methods=['POST'])
def update():
    blog_id = request.form['id']
    one = db.blogpostDB.find_one({'_id':ObjectId(blog_id)})

    db.blogpostDB.update_one({
            '_id': ObjectId(blog_id)
        },
        {
            '$set': {
                'title': request.form['title'],
                'post': request.form['post']
            }
        }, 
    upsert=False)

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    return JSONEncoder().encode(posts)


@app.route('/delete', methods=['POST'])
def delete():

    blog_id = request.form['id']

    one = db.blogpostDB.find_one({'_id':ObjectId(blog_id)})
    result = db.blogpostDB.delete_one({'_id':ObjectId(blog_id)})

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    for post in posts:
        print post
    #return JSONEncoder().encode(posts[-1])
    return JSONEncoder().encode(posts)


### Insert function here ###



############################



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
