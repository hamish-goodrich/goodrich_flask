from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Service_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    open = db.Column(db.Boolean)
    assigned = db.Column(db.String(200))
    urgency = db.Column(db.String(200))

    

class Monitoring_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pond_name = db.Column(db.String(400))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    weather = db.Column(db.String(40))
    temperature = db.Column(db.String(40))
    ibc_level = db.Column(db.Integer)

    forebay_sample = db.Column(db.Boolean)
    forebay_ph = db.Column(db.Float)
    forebay_ntu = db.Column(db.Float)
    forebay_temp = db.Column(db.Integer)
    forebay_height = db.Column(db.Integer)
    forebay_comments = db.Column(db.String(400))
    forebay_floc_dosed = db.Column(db.Integer)
    forebay_lime_dosed = db.Column(db.Integer)
    forebay_silt = db.Column(db.Integer)
    forebay_clear = db.Column(db.Boolean)
    forebay_cloudy = db.Column(db.Boolean)

    main_sample = db.Column(db.Boolean)
    main_ph = db.Column(db.Float)
    main_ntu = db.Column(db.Float)
    main_temp = db.Column(db.Integer)
    main_height = db.Column(db.Integer)
    main_comments = db.Column(db.String(400))
    main_floc_dosed = db.Column(db.Integer)
    main_lime_dosed = db.Column(db.Integer)
    main_silt = db.Column(db.Integer)
    main_clear = db.Column(db.Boolean)
    main_cloudy = db.Column(db.Boolean)

    flume_flow      = db.Column(db.Boolean)
    forebay_flow    = db.Column(db.Boolean)
    main_flow       = db.Column(db.Boolean)
    decant_flow     = db.Column(db.Boolean)

    unit_type = db.Column(db.String(40))
    floc_type = db.Column(db.String(40))
    author = db.Column(db.String(400))
    company = db.Column(db.String(400))
    week_ending = db.Column(db.String(40))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
