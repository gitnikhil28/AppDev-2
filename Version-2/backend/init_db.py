from flask import Flask
from models import db,User
from flask_bcrypt import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_admin_user():
    admin_user = User.query.filter_by(email='admin@gmail.com').first()
    if not admin_user:
        hashed_password = generate_password_hash('admin').decode('utf-8')  # Hash the password
        admin_user = User(username='admin', email='admin@gmail.com', password=hashed_password, role='admin')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")

with app.app_context():
    db.create_all()
    create_admin_user()