from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify, make_response
from flask_login import login_required, current_user
from .models import User, Service_request, Monitoring_log, Units, Ponds, Stocktake, Soil_testing, Job_cards
from . import db
import json
import csv
from io import StringIO
from datetime import datetime, timedelta

job_view = Blueprint('job_view', __name__)

@job_view.route('/job_cards', methods=['GET', 'POST'])
@login_required
def job_cards():
    return render_template("job_cards.html", user=current_user)

@job_view.route('/download_csv')
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
        headers={"Content-Disposition": "attachment; filename=job_cards.csv"}
    )