from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify
from flask_login import login_required, current_user
from .models import Note, Monitoring_log
from . import db
import json
import csv
from io import StringIO
from datetime import datetime, timedelta
import pendulum

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():

    return render_template("dashboard.html", user=current_user)

@views.route('/pond_monitoring', methods=['GET', 'POST'])
@login_required
def pond_monitoring():
    logs = Monitoring_log.query.all()  # Fetch all logs from DB
    # Get unique week endings from logs
    unique_weeks = sorted(set(log.week_ending for log in logs), reverse=True)
    # Get selected week from URL, default to the latest week
    selected_week = request.args.get("selected_week", unique_weeks[0] if unique_weeks else None)
    return render_template("pond_monitoring.html", logs=logs, unique_weeks=unique_weeks, selected_week=selected_week, user=current_user)

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

@views.route('/floc_units', methods=['GET', 'POST'])
@login_required
def floc_units():
    return render_template("floc_units.html", user=current_user)

@views.route("/view_log/<int:log_id>")
def view_log(log_id):
    log = Monitoring_log.query.get_or_404(log_id)  # Fetch log from database
    return render_template("view_log.html", log=log, user=current_user)

@views.route('/edit_log/<int:log_id>', methods=['GET', 'POST'])
def edit_log(log_id):
    log = Monitoring_log.query.get_or_404(log_id)

    if request.method == 'POST':
        log.date = request.form['date']
        dt = datetime.strptime(log.date, '%d/%m/%Y').date()
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        log.week_ending = end.strftime('%d/%b/%Y')

        log.time        = request.form['time']
        log.weather     = request.form['weather']
        log.temperature = request.form['temperature']
        log.ibc_level   = request.form['ibc_level']
        log.flume_flow  = 'flume_flow' in request.form  # True if checked, False otherwise
        log.forebay_flow = 'forebay_flow' in request.form  # True if checked, False otherwise
        log.main_flow   = 'main_flow' in request.form  # True if checked, False otherwise
        log.decant_flow = 'decant_flow' in request.form  # True if checked, False otherwise
        log.floc_type   = request.form['floc_type']
        log.unit_type   = request.form['unit_type']
        log.company     = request.form['company']
        log.author      = request.form['author']

        log.forebay_sample     = 'forebay_sample' in request.form  # True if checked, False otherwise
        log.forebay_ph         = request.form['forebay_ph']
        log.forebay_ntu        = request.form['forebay_ntu']
        log.forebay_temp       = request.form['forebay_temp']
        log.forebay_height     = request.form['forebay_height']
        log.forebay_comments   = request.form['forebay_comments']
        log.forebay_floc_dosed = request.form['forebay_floc_dosed']
        log.forebay_lime_dosed = request.form['forebay_lime_dosed']
        log.forebay_silt       = request.form['forebay_silt']

        log.main_sample     = 'main_sample' in request.form  # True if checked, False otherwise
        log.main_ph         = request.form['main_ph']
        log.main_ntu        = request.form['main_ntu']
        log.main_temp       = request.form['main_temp']
        log.main_height     = request.form['main_height']
        log.main_comments   = request.form['main_comments']
        log.main_floc_dosed = request.form['main_floc_dosed']
        log.main_lime_dosed = request.form['main_lime_dosed']
        log.main_silt       = request.form['main_silt']

        db.session.commit()
        return redirect(url_for('views.view_log', log_id=log.id, user=current_user))

    return render_template('edit_log.html', log=log, user=current_user)


@views.route('/delete-log', methods=['POST'])
def delete_log():
    log_id = request.form.get('id')  # Get the ID from the form submission
    if not log_id:
        return jsonify({"error": "Log ID is required"}), 400
    log_entry = Monitoring_log.query.get(log_id)
    if not log_entry:
        return jsonify({"error": "Log entry not found"}), 404
    db.session.delete(log_entry)
    db.session.commit()
    return redirect(url_for('views.pond_monitoring'))  # Redirect back to the home page


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
        dt = datetime.strptime(date, '%d/%m/%Y').date()
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        week_ending = end.strftime('%d/%b/%Y')
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
                                 author=current_user.full_name,
                                 week_ending=week_ending,)
        db.session.add(new_log)
        db.session.commit()
        flash('Log added', category='success')
        return redirect(url_for('views.pond_monitoring'))

    return render_template("createlog.html", user=current_user)

@views.route('/download_csv')
def download_csv():
    logs = Monitoring_log.query.all()

    # Create an in-memory file
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "pond_name", 
        "date", 
        "time", 
        "weather",
        "temperature",
        "ibc_level",  
        "forebay_sample", 
        "forebay_ph", 
        "forebay_ntu", 
        "forebay_temp", 
        "forebay_height",
        "forebay_comments",
        "forebay_floc_dosed",
        "forebay_lime_dosed",
        "forebay_silt",
        "forebay_clear",
        "forebay_cloudy",
        "main_sample",
        "main_ph",
        "main_ntu",
        "main_temp",
        "main_height",
        "main_comments",
        "main_floc_dosed",
        "main_lime_dosed",
        "main_silt",
        "main_clear",
        "main_cloudy",
        "flume_flow",
        "forebay_flow",
        "main_flow",
        "decant_flow",
        "unit_type",
        "floc_type",
        "author",
        "company",
        "week_ending",
    ])

    # Write data rows
    for log in logs:
        writer.writerow([
            log.pond_name,
            log.date,
            log.time,
            log.weather,
            log.temperature,
            log.ibc_level,
            log.forebay_sample,
            log.forebay_ph,
            log.forebay_ntu,
            log.forebay_temp,
            log.forebay_height,
            log.forebay_comments,
            log.forebay_floc_dosed,
            log.forebay_lime_dosed,
            log.forebay_silt,
            log.forebay_clear,
            log.forebay_cloudy,
            log.main_sample,
            log.main_ph,
            log.main_ntu,
            log.main_temp,
            log.main_height,
            log.main_comments,
            log.main_floc_dosed,
            log.main_lime_dosed,
            log.main_silt,
            log.main_clear,
            log.main_cloudy,
            log.flume_flow,
            log.forebay_flow,
            log.main_flow,
            log.decant_flow,
            log.unit_type,
            log.floc_type,
            log.author,
            log.company,
            log.week_ending],)
    
    output.seek(0)

    return Response(
        output, 
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=monitoring_logs.csv"}
    )

@views.route('/upload_log', methods=['POST'])
def upload_log():
    start = datetime
    end = datetime
    return jsonify({"message": "Log added successfully"}), 201
    try:
        data = request.get_json()  # Get JSON from Flutter
        date=data.get("date"),
        dt = datetime.strptime(date, '%d/%m/%Y').date(),
        start = dt - timedelta(days=dt.weekday()),
        end = start + timedelta(days=6),
        week_ending = end.strftime('%d/%b/%Y'),

        # Create a new Monitoring_log entry
        new_log = Monitoring_log(
        pond_name=data.get("pond_name"),
        date=date,
        week_ending = week_ending,
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
        forebay_silt=data.get("forebay_silt"),
        forebay_clear=data.get("forebay_clear"),
        forebay_cloudy=data.get("forebay_cloudy"),

        main_sample=data.get("main_sample"),
        main_ph=data.get("main_ph"),
        main_ntu=data.get("main_ntu"),
        main_temp=data.get("main_temp"),
        main_height=data.get("main_height"),
        main_comments=data.get("main_comments"),
        main_floc_dosed=data.get("main_floc_dosed"),
        main_lime_dosed=data.get("main_lime_dosed"),
        main_silt=data.get("main_silt"),
        main_clear=data.get("main_clear"),
        main_cloudy=data.get("main_cloudy"),

        flume_flow=data.get("flume_flow"),
        forebay_flow=data.get("forebay_flow"),
        main_flow=data.get("main_flow"),
        decant_flow=data.get("decant_flow"),

        unit_type=data.get("unit_type"),
        floc_type=data.get("floc_type"),
        author=data.get("author"),
        company=data.get("company"),
        )

        # Add to database
        db.session.add(new_log)
        db.session.commit()

        return jsonify({"message": "Log added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400