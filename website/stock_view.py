from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify, make_response
from flask_login import login_required, current_user
from .models import User, Service_request, Monitoring_log, Units, Ponds, Stocktake, Soil_testing, Job_cards
from . import db
import json
import csv
from io import StringIO
from datetime import datetime, timedelta

stock_view = Blueprint('stock_view', __name__)

@stock_view.route('/view_stock', methods=['GET', 'POST'])
@login_required
def view_stock():
    all_stock = Stocktake.query.all()
    return render_template("view_stock.html", all_stock=all_stock, user=current_user)

@stock_view.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        item = request.form.get('item')
        instock = request.form.get('instock')
        onorder = request.form.get('onorder')
        reorder_level = request.form.get('reorder_level')
        last_unit_price = request.form.get('last_unit_price')
        supplier = request.form.get('supplier')
        link = request.form.get('link')
        date = request.form.get('date')

        new_stock = Stocktake(
            item = item,
            instock = instock,
            onorder = onorder,
            reorder_level = reorder_level,
            last_unit_price = last_unit_price,
            supplier = supplier,
            link = link,
            # date = date,
        )

        db.session.add(new_stock)
        db.session.commit()
        return redirect(url_for('stock_view.view_stock'))

    return render_template('add_stock.html', user=current_user)

@stock_view.route('/edit_stock/<int:stock_id>', methods=['GET', 'POST'])
def edit_stock(stock_id):
    stock = Stocktake.query.get_or_404(stock_id)

    if request.method == 'POST':
        stock.item = request.form.get('item')
        stock.instock = request.form.get('instock')
        stock.onorder = request.form.get('onorder')
        stock.reorder_level = request.form.get('reorder_level')
        stock.last_unit_price = request.form.get('last_unit_price')
        stock.supplier = request.form.get('supplier')
        stock.link = request.form.get('link')
        stock.date = request.form.get('date')
        db.session.commit()
        return redirect(url_for('stock_view.view_stock', stock_id=stock.id, user=current_user))

    return render_template('edit_stock.html', stock=stock, user=current_user)


@stock_view.route('/delete_stock', methods=['POST'])
def delete_stock():
    stock_id = request.form.get('id')  # Get the ID from the form submission
    if not stock_id:
        return jsonify({"error": "stock is required"}), 400
    stock_entry = Stocktake.query.get(stock_id)
    if not stock_entry:
        return jsonify({"error": "stock_id not found"}), 404
    db.session.delete(stock_entry)
    db.session.commit()
    return redirect(url_for('stock_view.view_stock'))  # Redirect back to the home page