
from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models.models import Listing, Reminder
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    user_name = session.get('user_name', 'Guest')
    return render_template('index.html', user_name=user_name)

@main.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    reminders = Reminder.query.filter_by(user_id=user_id).all() if user_id else []
    return render_template('dashboard.html', user_name=session.get('user_name'), reminders=reminders)

@main.route('/create', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_listing = Listing(title=title, description=description)
        db.session.add(new_listing)
        db.session.commit()
        return redirect(url_for('main.listings'))
    return render_template('create_listing.html')

@main.route('/listings')
def listings():
    listings = Listing.query.all()
    return render_template('listings.html', listings=listings)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_listing(id):
    listing = Listing.query.get_or_404(id)
    if request.method == 'POST':
        listing.title = request.form['title']
        listing.description = request.form['description']
        db.session.commit()
        return redirect(url_for('main.listings'))
    return render_template('edit_listing.html', listing=listing)

@main.route('/reminder', methods=['GET', 'POST'])
def add_reminder():
    if request.method == 'POST':
        title = request.form['title']
        time = request.form['time']
        user_id = session.get('user_id')
        reminder = Reminder(title=title, time=time, user_id=user_id)
        db.session.add(reminder)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('reminder.html')
