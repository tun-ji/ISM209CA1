from main import db
from werkzeug.security import generate_password_hash, check_password_hash
# import models
from datetime import date


class User(db.Model):  # notice  that  our  class  extends  db.Model
    __tablename__ = 'userregister'   # this  is  the  name  we  want  the  table  in  database  to  have.
    id = db.Column(db.Integer,  primary_key=True)
    firstname = db.Column(db.String(20),  unique=False,  nullable=False)
    lastname = db.Column(db.String(20),  unique=False,  nullable=False)
    othernames = db.Column(db.String(20),  unique=False,  nullable=True)
    email = db.Column(db.String(50),  unique=True,  nullable=False)
    password = db.Column(db.String(256),  unique=False,  nullable=False)

    #  represent  the  object  when  it  is  queried  for
    def __repr__(self):
        return '<Register  {}>'.format(self.id)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Customers(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(20), unique=False, nullable=False)
    Surname = db.Column(db.String(20), unique=False, nullable=False)
    Date_of_Birth = db.Column(db.Date, nullable=False, default=date.today())
    Residential_address = db.Column(db.Text, unique=False, nullable=False)
    Nationality = db.Column(db.String(20), unique = False, nullable=False)
    National_Identification_Number = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Customer {}>'.format(self.id)