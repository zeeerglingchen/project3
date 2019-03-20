import csv
import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movies.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

row_lst = []
with open("movies_clean.csv","r") as csvdata:
    reader = csv.reader(csvdata)
    for row in reader:
        row_lst.append(row)

# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy

class Movie(db.Model):
    __tablename__ = "movies"
    Id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    Title = db.Column(db.String(64),nullable=False)
    Date = db.Column(db.String(64))
    Distributor = db.Column(db.String(64))
    IMDBRating = db.Column(db.Integer)
    IMDBVotes = db.Column(db.Integer)

    Genre_id = db.Column(db.Integer,db.ForeignKey("genres.Id"))
    Director_id = db.Column(db.Integer,db.ForeignKey("directors.Id"))
    MPAARating_id = db.Column(db.Integer,db.ForeignKey("mpaarating.Id"))
    genre = db.relationship("Genre")
    director = db.relationship("Director")
    mpaarating = db.relationship("MPAARating")

    # wonder what will the foriegnkey return
    def __repr__(self):
        return "{} movie {} by {} | Released on {} | MPAA Rating is {}".format(self.Genre_id, self.Title, self.Director_id, self.Date, self.MPAARating_id )

class Genre(db.Model):
    __tablename__ = "genres"
    Id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    GenreName = db.Column(db.String(64))

    def __repr__(self):
        return"The Genre is {}".format(self.GenreName)


class Director(db.Model):
    __tablename__ = "directors"
    Id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    DirectorName = db.Column(db.String(64))

    def __repr__(self):
        return"The Director is {}".format(self.DirectorName)


class MPAARating(db.Model):
    __tablename__ = "mpaarating"
    Id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    MPAA_Rating = db.Column(db.String(64))

    def __repr__(self):
        return"The MPAA Rating is {}".format(self.Rating)

# //先简历数据库，后插入data
if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that

# #insert data to database

for i in row_lst[1:]:
    director_data = Director.query.filter_by(DirectorName = i[12]).first()
    if director_data :
        pass
    else:
        director_data = Director(
        DirectorName = i[12])

    genre_data = Genre.query.filter_by(GenreName = i[10]).first()
    if genre_data:
        pass
    else:
        genre_data = Genre(
        GenreName = i[10])

    rating_data =  MPAARating.query.filter_by(MPAA_Rating = i[6]).first()
    if rating_data:
        pass
    else:
        rating_data = MPAARating(
        MPAA_Rating = i[6]
    )

    session.add(director_data)
    session.add(genre_data)
    session.add(rating_data)

session.commit()

for i in row_lst[1:]:
    director_data = Director.query.filter_by(DirectorName = i[12]).first()
    genre_data = Genre.query.filter_by(GenreName = i[10]).first()
    rating_data =  MPAARating.query.filter_by(MPAA_Rating = i[6]).first()
    moive_data = Movie(
            Title = i[0],
            Date = i[5],
            Distributor = i[8],
            IMDBRating = i[-2],
            IMDBVotes = i[-1],
            Genre_id = genre_data.Id,
            Director_id = director_data.Id,
            MPAARating_id = rating_data.Id
        )
    session.add(moive_data)
session.commit()

def create_or_get_directors(name):
    director = Director.query.filter_by(DirectorName = name).first()
    if director:
        return director
    else:
        add_director = Director(DirectorName = name)
        session.add(add_director)
        session.commit()
        return add_director
        # why

def create_or_get_genre(name):
    genre = Genre.query.filter_by(GenreName = name).first()
    if genre:
        return genre
    else:
        add_genre = Genre(GenreName = name)
        session.add(add_genre)
        session.commit()
        return add_genre


@app.route('/')
def index():
    test = Movie.query.all()
    num_movies = len(test)
    return render_template("index.html",num_movies = num_movies)


@app.route('/moives/new/<title>/<director>/<genre>/')
def add_moive(title,director,genre):
    if Movie.query.filter_by(Title = title).first():
        return "The movie already exists in this data base"
    else:
        new_di = create_or_get_directors(director)
        new_gen = create_or_get_genre(genre)
        new_movie = Movie (Title = title, Genre_id = new_gen.Id, Director_id = new_di.Id)
        session.add(new_movie)
        session.commit()
        return "new movie {} has been added".format(new_movie.Title)

@app.route('/all_mpaaratings')
def all_ratings():
    ratingtypes = []
    rating = MPAARating.query.all();
    for r in rating:
        ratingtypes.append(r.MPAA_Rating)
    return str(ratingtypes)








if __name__ == '__main__':
    app.run()
