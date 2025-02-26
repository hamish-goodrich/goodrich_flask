from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify, make_response
from flask_login import login_required, current_user
from .models import Service_request, Monitoring_log, Units
from . import db
import json
import csv
from io import StringIO
from datetime import datetime, timedelta

job_view = Blueprint('job_view', __name__)
