from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Person(db.Model):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)

class Planet(db.Model):
    __tablename__ = 'planet'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)

class Favorito(db.Model):
    __tablename__ = 'favorito'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship(Person)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)