from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify, make_response
from flask_login import login_required, current_user
from .models import User, Service_request, Monitoring_log, Units, Ponds, Stocktake, Soil_testing, Job_cards
from . import db
import json
import csv
from io import StringIO
from datetime import datetime, timedelta

stock_view = Blueprint('stock_view', __name__)

@stock_view.route('/stock_view', methods=['GET', 'POST'])
@login_required
def stock_take():
    return render_template("stock_view.html", user=current_user)