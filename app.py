from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'abc' # random string

db = SQLAlchemy(app)
hashids = Hashids(min_length=5, salt=app.config['SECRET_KEY'])

# data model: helps us create the database by itself
class Urls(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    long = db.Column('long', db.String())
    short = db.Column('short', db.String())
    created_on = db.Column(db.DateTime())

    def __init__(self, long, short, created_on=None):
        self.long = long
        self.short = short
        self.created_on = datetime.now()

def get_shorten_url(row_id):
    '''shorten url based on id of that row'''
    hashid = hashids.encode(row_id)
    short_url = request.host_url + hashid
    return short_url

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        long_url_received = request.form['url']

        # check if long url exist in DB
        found_url = Urls.query.filter_by(long=long_url_received).first()

        if found_url: # refactor to url_row
            return render_template('home.html', short_url=found_url.short)
        else:
            new_url = Urls(long_url_received, None)
            db.session.add(new_url)
            db.session.commit()

            short_url = get_shorten_url(new_url.id)
            new_url.short = short_url
            db.session.commit()
            return render_template('home.html', short_url=short_url)

    return render_template('home.html')

@app.route('/<id>')
def url_redirect(id):
    original_id = hashids.decode(id) # decode returns a tuple
    if original_id:
        original_id = original_id[0]
        data = Urls.query.filter_by(id=original_id).first()
        long_url = data.long
        return redirect(long_url)
    else:
        flash("Invalid URL")
        return redirect(url_for('home'))

@app.route('/stats')
def stats():
    url_records = Urls.query.all()
    return render_template('stats.html', url_records=url_records)

if __name__ == '__main__':
    app.run(port=5000, debug=True)