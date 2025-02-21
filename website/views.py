from flask import Blueprint, render_template, request, flash, jsonify, Response
from flask_login import login_required, current_user
from .models import Note, Monitoring_log
from . import db
import json
import csv
from io import StringIO

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    # logs = Monitoring_log.query
    # if request.method == 'POST': 
    #     note = request.form.get('note')#Gets the note from the HTML 

    #     if len(note) < 1:
    #         flash('Note is too short!', category='error') 
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
    #         db.session.add(new_note) #adding the note to the database 
    #         db.session.commit()
    #         flash('Note added!', category='success')

    return render_template("dashboard.html", user=current_user)

@views.route('/pond_monitoring', methods=['GET', 'POST'])
@login_required
def pond_monitoring():
    return render_template("pond_monitoring.html", user=current_user)

@views.route('/bench_testing', methods=['GET', 'POST'])
@login_required
def bench_testing():
    return render_template("bench_testing.html", user=current_user)

@views.route('/service_requests', methods=['GET', 'POST'])
@login_required
def service_requests():
    return render_template("service_requests.html", user=current_user)

@views.route('/stock_take', methods=['GET', 'POST'])
@login_required
def stock_take():
    return render_template("stock_take.html", user=current_user)

@views.route('/job_cards', methods=['GET', 'POST'])
@login_required
def job_cards():
    return render_template("job_cards.html", user=current_user)



@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/createlog', methods=['GET', 'POST'])
@login_required
def createlog():

    if request.method == 'POST':
        pond_name    = request.form.get('pond_name')
        date    = request.form.get('date')
        time    = request.form.get('time')
        weather = request.form.get('weather')
        temperature = request.form.get('temperature')
        forebay_ph = request.form.get('forebay_ph')
        forebay_ntu =request.form.get('forebay_ntu')
        main_ph = request.form.get('main_ph')
        main_ntu = request.form.get('main_ntu')
        ibc_level = request.form.get('ibc_level')

        new_log = Monitoring_log(pond_name=pond_name, 
                                 date=date, 
                                 time=time, 
                                 weather=weather, 
                                 temperature=temperature, 
                                 forebay_ph=forebay_ph,
                                 forebay_ntu=forebay_ntu,
                                 main_ph=main_ph,
                                 main_ntu=main_ntu,
                                 ibc_level=ibc_level, 
                                 author=current_user.full_name)
        db.session.add(new_log)
        db.session.commit()
        flash('Log added', category='success')
        return redirect(url_for('views.home'))

    return render_template("createlog.html", user=current_user)

@views.route('/download_csv')
def download_csv():
    logs = Monitoring_log.query.all()

    # Create an in-memory file
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "ID", "Pond Name", "Date", "Time", "Temperature", "Forebay pH", "Forebay NTU", 
        "Main pH", "Main NTU", "IBC Level", "Author"
    ])
    
    # Write data rows
    for log in logs:
        writer.writerow([
            log.id, log.pond_name, log.date, log.time, log.temperature, 
            log.forebay_ph, log.forebay_ntu, log.main_ph, log.main_ntu, 
            log.ibc_level, log.author
        ])
    
    output.seek(0)

    return Response(
        output, 
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=monitoring_logs.csv"}
    )

@views.route('/upload_log', methods=['POST'])
def upload_log():
    try:
        data = request.get_json()  # Get JSON from Flutter

        # Create a new Monitoring_log entry
        new_log = Monitoring_log(
            pond_name=data.get("pond_name"),
            date=data.get("date"),
            time=data.get("time"),
            weather=data.get("weather"),
            temperature=data.get("temperature"),
            ibc_level=data.get("ibc_level"),
            forebay_sample=data.get("forebay_sample"),
            forebay_ph=data.get("forebay_ph"),
            forebay_ntu=data.get("forebay_ntu"),
            forebay_temp=data.get("forebay_temp"),
            forebay_height=data.get("forebay_height"),
            forebay_comments=data.get("forebay_comments"),
            forebay_floc_dosed=data.get("forebay_floc_dosed"),
            forebay_lime_dosed=data.get("forebay_lime_dosed"),
            main_sample=data.get("main_sample"),
            main_ph=data.get("main_ph"),
            main_ntu=data.get("main_ntu"),
            main_temp=data.get("main_temp"),
            main_height=data.get("main_height"),
            main_comments=data.get("main_comments"),
            main_floc_dosed=data.get("main_floc_dosed"),
            main_lime_dosed=data.get("main_lime_dosed"),
            flume_flow=data.get("flume_flow"),
            forebay_flow=data.get("forebay_flow"),
            main_flow=data.get("main_flow"),
            decant_flow=data.get("decant_flow"),
            unit_type=data.get("unit_type"),
            floc_type=data.get("floc_type"),
            author=data.get("author")
        )

        # Add to database
        db.session.add(new_log)
        db.session.commit()

        return jsonify({"message": "Log added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400