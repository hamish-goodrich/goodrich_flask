from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify, make_response
from flask_login import login_required, current_user
from .models import Service_request, Monitoring_log, Units
from . import db
import json
import csv
from io import StringIO
from datetime import datetime, timedelta

views = Blueprint('views', __name__)
    
@views.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

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

