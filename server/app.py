#!/usr/bin/env python3

from flask import Flask, request
from flask_migrate import Migrate

from models import db, Activity, Signup, Camper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Hey Man</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    
@app.route('/campers', methods=['GET', 'POST'])
def campers():
    campers = Camper.query.all()
    
    if request.method == 'GET':
        return [camper.to_dict() for camper in campers]
    
    elif request.method == 'POST':
        try:        
            new_camper = Camper(**request.json)
            db.session.add(new_camper)
            db.session.commit()
            return new_camper.to_dict(), 201
        except ValueError:
            return {'error': '400: Request Failed'}, 400
    
@app.route('/campers/<int:camper_id>', methods=['GET', 'PATCH', 'DELETE'])
def camper_by_id(camper_id):
    camper = Camper.query.filter_by(id=camper_id).first()
    
    if camper is None:
        return {'error': 'Camper not found'}, 404
    
    elif request.method == 'GET':
        return camper.to_dict()
    
    elif request.method == 'PATCH':
        for key, value in request.json.items():
            setattr(camper, key, value)
        db.session.commit()
        return camper.to_dict(), 202
    
    elif request.method == 'DELETE':
        db.session.delete(camper)
        db.session.commit()
        return camper.to_dict(), 204
    
@app.route('/activities', methods=['GET', 'POST'])
def activities():
    activities = Activity.query.all()
    
    if request.method == 'GET':
        return [activity.to_dict() for activity in activities]
    
    elif request.method == 'POST':
        new_activity = Activity(**request.json)
        db.session.add(new_activity)
        db.session.commit()
        return new_activity.to_dict(), 201
    
@app.route('/activities/<int:activity_id>', methods=['GET', 'PATCH', 'DELETE'])
def activity_by_id(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    
    if activity is None:
        return {'error': 'Activity not found'}, 404
    
    elif request.method == 'GET':
        return activity.to_dict()
    
    elif request.method == 'PATCH':
        for key, value in request.json.items():
            setattr(activity, key, value)
        db.session.commit()
        return activity.to_dict(), 202
    
    elif request.method == 'DELETE':
        db.session.delete(activity)
        db.session.commit()
        return activity.to_dict(), 204
    
@app.route('/signups', methods=['GET', 'POST'])
def signups():
    signups = Signup.query.all()
    
    if request.method == 'GET':
        return [signup.to_dict() for signup in signups]
    
    elif request.method == 'POST':
        try:
            new_signup = Signup(**request.json)
            db.session.add(new_signup)
            db.session.commit()
            return new_signup.to_dict(), 201
        except ValueError:
            return {'error': '400: Request Failed'}, 400
        
