from flask import Flask, render_template , url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import os

SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_image_list(path) :
    image_list = os.listdir(path)
    return image_list

app = Flask(__name__)
app.config['image_name'] = 'swan'
app.config['image_list'] = create_image_list('./static/pictures/')
app.config['attributes'] = pd.read_csv("./static/attributes/NOWHERE_DATASET.csv", header=[0, 1], index_col=0)
# Should we use a sqllite database istead of a pandas library

@app.route('/',methods=['POST','GET'])
def index():




    if request.method == "POST":
        app.config['image_name'] = request.form["content"]
        return redirect('/')

    else:
        image_name = app.config['image_name']
        PEOPLE_FOLDER = os.path.join('static', 'pictures')
        picture_filename = image_name + '.jpg'
        full_filename = os.path.join(PEOPLE_FOLDER , picture_filename)

        image_list = app.config['image_list']

        db_attributes = app.config['attributes']




        return render_template('index.html', image = image_name ,user_image = full_filename, image_list = image_list )

if __name__ == "__main__":
    app.run(debug = True)
