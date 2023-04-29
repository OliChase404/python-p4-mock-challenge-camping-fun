from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'
    serialize_rules = ('-campers.signups', '-signups.activity')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    signups = db.relationship('Signup', backref='activity')
    campers = association_proxy('signups', 'camper', creator=lambda c: Signup(camper=c))


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'
    serialize_rules = ('-activity.signups', '-camper.signups')
    
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    @validates('time')
    def validate_time(self, key, time):
        if time in range(0, 24):
            return time
        else: 
            raise ValueError('Time must be between 0 and 23')
    

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'
    serialize_rules = ('-activities.campers', '-signups.camper')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    signups = db.relationship('Signup', backref='camper')
    activities = association_proxy('signups', 'activity', creator=lambda a: Signup(activity=a))
    
    @validates('age')
    def validate_age(self, key, age):
        if age in range(8, 19):
            return age
        else:
            raise ValueError('Age must be between 8 and 18')
        
    @validates('name')
    def validate_name(self, key, name):
        if name:
            return name
        else:
            raise ValueError('Name must not be empty')

