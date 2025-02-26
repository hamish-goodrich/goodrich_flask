from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify, make_response
from flask_login import login_required, current_user
from .models import Service_request, Monitoring_log, Units
from . import db
import json
import csv
from io import StringIO
from datetime import datetime, timedelta

unit_view = Blueprint('unit_view', __name__)

@unit_view.route('/view_units')
def view_units():
    units = Units.query.all()
    return render_template('view_units.html', units=units, user=current_user)

@unit_view.route('/add-unit', methods=['GET', 'POST'])
def add_unit():
    if request.method == 'POST':
        unit = request.form.get('unit')
        unit_type = request.form.get('unit_type')
        modem_id = request.form.get('modem_id')
        rut_sn = request.form.get('rut_sn')
        rut_mac = request.form.get('rut_mac')
        rut_carrier = request.form.get('rut_carrier')
        rut_sim = request.form.get('rut_sim')
        rut_phone = request.form.get('rut_phone')

        new_unit = Units(
            unit=unit,
            unit_type=unit_type,
            modem_id=modem_id,
            rut_sn=rut_sn,
            rut_MAC=rut_mac,
            rut_carrier=rut_carrier,
            rut_sim=rut_sim,
            rut_phone=rut_phone,
        )

        db.session.add(new_unit)
        db.session.commit()
        flash('Unit added successfully!', 'success')
        return redirect(url_for('unit_view.view_units'))

    return render_template('add_unit.html', user=current_user)

@unit_view.route('/edit_unit/<int:unit_id>', methods=['GET', 'POST'])
def edit_unit(unit_id):
    unit = Units.query.get_or_404(unit_id)

    if request.method == 'POST':
        unit.unit = request.form.get('unit')
        unit.unit_type = request.form.get('unit_type')
        unit.modem_id = request.form.get('modem_id')
        unit.rut_sn = request.form.get('rut_sn')
        unit.rut_MAC = request.form.get('rut_mac')
        unit.rut_carrier = request.form.get('rut_carrier')
        unit.rut_sim = request.form.get('rut_sim')
        unit.rut_phone = request.form.get('rut_phone')
        db.session.commit()
        return redirect(url_for('unit_view.view_units', unit_id=unit.id, user=current_user))

    return render_template('edit_unit.html', unit=unit, user=current_user)


@unit_view.route('/delete-unit', methods=['POST'])
def delete_unit():
    unit_id = request.form.get('id')  # Get the ID from the form submission
    if not unit_id:
        return jsonify({"error": "Unit ID is required"}), 400
    unit_entry = Units.query.get(unit_id)
    if not unit_entry:
        return jsonify({"error": "Unit not found"}), 404
    db.session.delete(unit_entry)
    db.session.commit()
    return redirect(url_for('unit_view.view_units'))  # Redirect back to the home page