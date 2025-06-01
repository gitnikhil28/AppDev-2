from app import celery_app
from models import db, User
from celery_context import flaskContext
from celery import Celery
from io import StringIO
from celery.schedules import crontab
from flask_mail import Mail, Message
from flask import url_for,jsonify
from models import db, User, InfluencerProfile, Campaign, AdRequest
import app

def send_email(to, subject, body, is_html=False):
    with app.app_context():  
        msg = Message(subject=subject, recipients=[to], html=body if is_html else None)
        mail.send(msg)


@celery_app.task()
def celeryIndex():
    
    print("Hello from celery")
    print("Good rey")

@celery_app.task()
def plus(a,b):
    return a + b

@celery_app.task(base=flaskContext)
def dbUpdate():
    new_data = User(email="hey@gmail.com", password="123", role="influencer",username="dun12")
    db.session.add(new_data)
    db.session.commit()
    return "Data added successfully", True

@celery_app.task()
def reminder():
    from app import mailer
    from models import User
    test_user = User.query.filter_by(email='inf1@gmail.com').first()
    if test_user:
        from flask_mail import Message
        
        msg = Message(subject='Reminder', body='This is a reminder', recipients=[test_user.email])
        mailer.send(msg)
        return "Reminder sent successfully", True
    return "No user found", False


@celery_app.task
# def send_ad_request_reminders():
#     with celery_app.app_context():  # Establish app context for database access
#         influencers = User.query.filter_by(role='influencer').all()
#         for influencer in influencers:
#             pending_requests = AdRequest.query.filter_by(influencer_id=influencer.id, status='Pending').all()
#             if pending_requests:
#                 # Send reminder email
#                 send_email(
#                     to=influencer.email,
#                     subject="Pending Ad Requests Reminder",
#                     body=f"Hello {influencer.username},\nYou have pending ad requests on IESCP. Please log in to view and take action on them."
#                 )

# @celery_app.task
# def send_monthly_activity_report():
#     with celery_app.app_context():
#         sponsors = User.query.filter_by(role='sponsor').all()
#         for sponsor in sponsors:
            
#             campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
#             report_data = {
#                 'sponsor_name': sponsor.username,
#                 'campaigns': [{
#                     'name': campaign.name,
#                     'start_date': campaign.start_date,
#                     'end_date': campaign.end_date,
#                     'budget': campaign.budget
#                     # Add other relevant campaign details here
#                 } for campaign in campaigns]
#             }

#             # Render HTML report (example)
#             from jinja2 import Environment, FileSystemLoader
#             env = Environment(loader=FileSystemLoader('templates'))  # Assuming your templates are in a 'templates' folder
#             template = env.get_template('monthly_report.html')
#             html_report = template.render(report_data)

#             # Send email with report
#             send_email(
#                 to=sponsor.email,
#                 subject="Monthly Activity Report",
#                 body=html_report,
#                 is_html=True
#             )


