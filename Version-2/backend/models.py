from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False) 
    is_approved = db.Column(db.Boolean, default=False)
    is_flagged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    niche = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(50), nullable=False)  # public/private
    goals = db.Column(db.Text, nullable=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_flagged = db.Column(db.Boolean, default=False)

    sponsor = db.relationship('User', backref=db.backref('campaigns', lazy=True))

class AdRequest(db.Model):
    __tablename__ = 'ad_requests'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    messages = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')  # Pending/Accepted/Rejected
    by_sponsor = db.Column(db.Boolean, nullable=False, default=False)  # New column
    name = db.Column(db.String(200), nullable=True)
    negotiated_price = db.Column(db.Float, nullable=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor_profiles.id'),nullable=True)

    campaign = db.relationship('Campaign', backref=db.backref('ad_requests', lazy=True))
    influencer = db.relationship('User', backref=db.backref('ad_requests', lazy=True))
    sponsor = db.relationship('SponsorProfile', backref=db.backref('ad_requests', lazy=True))

class SponsorProfile(db.Model):
    __tablename__ = 'sponsor_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=True)  # The budget of the sponsor for campaigns

    user = db.relationship('User', backref=db.backref('sponsor_profile', uselist=False))

    def __repr__(self):
        return f'<SponsorProfile {self.company_name}>'



class InfluencerProfile(db.Model):
    __tablename__ = 'influencer_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    niche = db.Column(db.String(200), nullable=True)
    reach = db.Column(db.Integer, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    profile_picture = db.Column(db.String(300), nullable=True)
    
    


    user = db.relationship('User', backref=db.backref('influencer_profile', uselist=False))


