from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id_user = db.Column(db.Integer, primary_key=True , nullable=False)
    name= db.Column(db.String(50), nullable=False)
    last_name= db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    date_of_suscription= db.Column(db.Date,nullable=False)
    favorite= db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id_user": self.id_user,
            "email": self.email,
            "date_of_suscription": self.date_of_suscription.strftime("%Y-%m-%d")

            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
   
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id_character'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id_planet'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id_vehicle'))
    
    def __repr__(self):
        return '<Favorite %r>' % self.id
    
    def serialize(self):
        return {
            "id_favorite": self.id,
            "character_id": self.character_id,
            "user_id": self.user_id,
            "planet_id": self.planet_id

            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
   
    id_character = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    eye = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    character= db.relationship('Favorite', backref='character', lazy=True)
   
    def __repr__(self):
        return '<Character %r>' % self.name
    
    def serialize(self):
        return {
            "id_character": self.id_character,
            "name": self.name,
            "eye": self.eye,
            "gender": self.gender
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
   
    id_planet= db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    planet= db.relationship('Favorite', backref='planet', lazy=True)
   
    def __repr__(self):
        return '<Character %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id_planet,
            "name": self.name

            # do not serialize the password, its a security breach
        }
    
class Vehicle(db.Model):
    __tablename__ = 'vehicle'
   
    id_vehicle = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    model = db.Column(db.String(50), unique=False, nullable=False)
    size = db.Column(db.Integer, unique=False, nullable=False)
    vehicle= db.relationship('Favorite', backref='vehicle', lazy=True)
   
    def __repr__(self):
        return '<Character %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id_vehicle,
            "name": self.name

            # do not serialize the password, its a security breach
        }