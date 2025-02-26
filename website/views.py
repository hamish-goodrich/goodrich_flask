from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify, make_response
from flask_login import login_required, current_user
from .models import User, Service_request, Monitoring_log, Units, Ponds, Stocktake, Soil_testing, Job_cards
from . import db
import json
import csv
from io import StringIO
from datetime import datetime, timedelta

views = Blueprint('views', __name__)
    
@views.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    all_users = User.query.all()
    all_ponds = Ponds.query.all()
    all_job_cards = Job_cards.query.all()
    all_units = Units.query.all()

    return render_template("dashboard.html", user=current_user, all_units=all_units, all_job_cards=all_job_cards, all_ponds=all_ponds, all_users=all_users)

@views.route('/bench_testing', methods=['GET', 'POST'])
@login_required
def bench_testing():
    return render_template("bench_testing.html", user=current_user)

@views.route('/service_requests', methods=['GET', 'POST'])
@login_required
def service_requests():
    return render_template("service_requests.html", user=current_user)





