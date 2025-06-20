#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    events = Event.query.all()
    events_list = []
    for event in events:
        event_dict = {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        events_list.append(event_dict)
    
    return jsonify(events_list), 200


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.filter(Event.id==id).first()
    if not event:
         return jsonify({"error": "Event not found"}), 404
    
    sessions_list = []
    for session in event.sessions:
        session_dict = {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat() if session.start_time else None
        }
        sessions_list.append(session_dict)
    return jsonify(sessions_list), 200  

    

@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()
    speakers_list = []
    for speaker in speakers:
        speaker_dict = {
            "id": speaker.id,
            "name": speaker.name
        }
        speakers_list.append(speaker_dict)
    return jsonify(speakers_list), 200


@app.route('/speakers/<int:id>')
def get_speaker_with_bio(id):
    speaker = Speaker.query.filter(Speaker.id==id).first()
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404
    
    sessions_list = []
    for session in speaker.sessions:
        session_dict = {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat() if session.start_time else None
        }
        sessions_list.append(session_dict)
    
    speaker_data = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available",
        "sessions": sessions_list
    }
    return jsonify(speaker_data), 200



@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.filter(Session.id==id).first()
    if not session:
        return jsonify({"error": "Session not found"}), 404

    speakers_list = []
    for speaker in session.speakers:
        speaker_dict = {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
        }
        speakers_list.append(speaker_dict)

    return jsonify(speakers_list), 200
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)