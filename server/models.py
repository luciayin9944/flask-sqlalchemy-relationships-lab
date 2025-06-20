from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# TODO: add association table
# table for many-to-many relationship between Session and Speaker
class SessionSpeaker(db.Model):
    __tablename__ = 'session_speakers'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    #relationship
    session = db.relationship('Session', back_populates='session_speakers')
    speaker = db.relationship('Speaker', back_populates='session_speakers')



# TODO: set up relationships for all models
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

     # Relationship: Event -> Sessions
    sessions = db.relationship('Session', back_populates='event', cascade="all, delete")

    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'
    

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # Relationship: Sessions -> Event
    event = db.relationship('Event', back_populates='sessions')

    # Relationship: Session <-> Speakers (Many-to-Many)
    session_speakers = db.relationship('SessionSpeaker', back_populates='session', cascade="all, delete-orphan")
    #speakers = association_proxy('session_speakers', 'speaker')
    speakers = association_proxy(
        'session_speakers', 'speaker',
        creator=lambda speaker: SessionSpeaker(speaker=speaker)
    )


    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'


class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # # One-to-one relationship to Bio
    bio = db.relationship('Bio', uselist=False, back_populates='speaker', cascade="all, delete-orphan")

    # # Many-to-many relationship to Sessions <-> speaker
    session_speakers = db.relationship('SessionSpeaker', back_populates='speaker', cascade="all, delete-orphan")
    #sessions = association_proxy('session_speakers', 'session')
    sessions = association_proxy(
        'session_speakers', 'session',
        creator=lambda session: SessionSpeaker(session=session)
    )
    

    def __repr__(self):
        return f'<Speaker {self.id}, {self.name}>'
    


class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    # One-to-one relationship to speaker
    speaker = db.relationship('Speaker', back_populates='bio')

    def __repr__(self):
        return f'<Bio {self.id}, {self.bio_text}>'
