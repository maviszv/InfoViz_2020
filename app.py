from flask import Flask, render_template , url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_image_list(path) :
    image_list = os.listdir(path)
    return image_list



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swan.db'
app.config['image_list'] = create_image_list('./static/pictures/')
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable= False )
    date_created = db.Column(db.DateTime, default= datetime.utcnow )

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():
    #It needs some error handeling
    if request.method == "POST":
        image_name = request.form["content"]
        image_name = Todo(name = image_name)
        try:
            db.session.add(image_name)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task!"

    else:
        message = Todo.query.order_by(Todo.date_created.desc()).first()
        PEOPLE_FOLDER = os.path.join('static', 'pictures')
        picture_filename = message.name + '.jpg'
        full_filename = os.path.join(PEOPLE_FOLDER , picture_filename)

        image_list = app.config['image_list']

        return render_template('index.html', image = message ,user_image = full_filename, image_list = image_list )

if __name__ == "__main__":
    app.run(debug = True)
