from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Generalized Many-to-Many Association Table
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assigned_id = db.Column(db.Integer, nullable=False)  # ID of the assigned item
    assigned_type = db.Column(db.String(50), nullable=False)  # Model name of the assigned item
    owner_id = db.Column(db.Integer, nullable=False)  # ID of the owner item
    owner_type = db.Column(db.String(50), nullable=False)  # Model name of the owner item

    def __repr__(self):
        return f'<Assignment {self.owner_type}({self.owner_id}) -> {self.assigned_type}({self.assigned_id})>'
    
# Soil Testing Model
class Soil_testing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    open = db.Column(db.Boolean)
    urgency = db.Column(db.String(200))
    location = db.Column(db.String(400))
    
    # pH and NTU Measurements at Different Depths
    phA10 = db.Column(db.Float)
    phB10 = db.Column(db.Float)
    phC10 = db.Column(db.Float)
    phD10 = db.Column(db.Float)
    phE10 = db.Column(db.Float)
    phF10 = db.Column(db.Float)
    phG10 = db.Column(db.Float)
    ntuA10 = db.Column(db.Float)
    ntuB10 = db.Column(db.Float)
    ntuC10 = db.Column(db.Float)
    ntuD10 = db.Column(db.Float)
    ntuE10 = db.Column(db.Float)
    ntuF10 = db.Column(db.Float)
    ntuG10 = db.Column(db.Float)
    
    # Image URLs
    image10url = db.Column(db.String(200))
    image30url = db.Column(db.String(200))
    image60url = db.Column(db.String(200))

    dose_rate = db.Column(db.String(200))
    

# Stocktake Model
class Stocktake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100))
    instock = db.Column(db.Integer)
    onorder = db.Column(db.Integer)
    reorder_level = db.Column(db.Integer)
    last_unit_price = db.Column(db.Integer)
    supplier = db.Column(db.String(200))
    link = db.Column(db.String(200))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

# Service Request Model
class Service_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    open = db.Column(db.Boolean)
    urgency = db.Column(db.String(200))

# Monitoring Log Model
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

    # Flow Data
    flume_flow = db.Column(db.Boolean)
    forebay_flow = db.Column(db.Boolean)
    main_flow = db.Column(db.Boolean)
    decant_flow = db.Column(db.Boolean)

    unit_type = db.Column(db.String(40))
    floc_type = db.Column(db.String(40))
    author = db.Column(db.String(400))
    company = db.Column(db.String(400))
    week_ending = db.Column(db.String(40))

    image_url = db.Column(db.String(500))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(200))

    admin = db.Column(db.Boolean)
    sudo = db.Column(db.Boolean)


# Ponds Model
class Ponds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pond_name = db.Column(db.String(400))
    group_name = db.Column(db.String(400))
    company = db.Column(db.String(400))
    pond_size = db.Column(db.Integer)
    catchment_area = db.Column(db.Integer)
    location = db.Column(db.Integer)
    estimated_duration = db.Column(db.Integer)
    monitoring_frequency=(db.String(400))
    image_url = db.Column(db.String(500))


# Units Model
class Units(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(400))
    unit_type = db.Column(db.String(400))
    modem_id = db.Column((db.String(40)))
    rut_sn = db.Column(db.String(40))
    rut_MAC = db.Column(db.String(40))
    rut_carrier = db.Column(db.String(40))
    rut_sim = db.Column(db.String(50))
    rut_phone = db.Column(db.String(40))
    last_serviced = db.Column(db.String(40))
    issue_list = db.Column(db.String(500))
    image_url = db.Column(db.String(500))

# Units Model
class Job_cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pond_name = db.Column(db.String(400))
    unit = db.Column(db.String(400))
    unit_type = db.Column(db.String(400))
    date = db.Column(db.String(50))
    author = db.Column(db.String(400))
    company = db.Column(db.String(400))
    in_out = db.Column(db.String(50))
    comments = db.Column(db.String(500))
    unit_type = db.Column(db.String(40))
    floc_type = db.Column(db.String(40))
