from flask import Flask, render_template, request, redirect
from models import db, User, Journey, FuelLog

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/log-journey', methods = ['GET', 'POST'])
def log_journey(): 
    if request.method == 'POST':
        ...
    return render_template('log_journey.html')

@app.route('/log-fuel', methods = ['GET', 'POST'])
def log_fuel():
    if request.method == 'POST':
        ...
    return render_template('log_fuel.html')

if __name__ == '__main__':
    app.run(debug = True)