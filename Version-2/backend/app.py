from flask import Flask,url_for,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
import csv




from celery import Celery
from config import config

from flask_mail import Mail, Message
from celery.schedules import crontab



from models import db,User, InfluencerProfile, SponsorProfile, AdRequest, Campaign
from routes.auth import Register, Login
from routes.admin import ApproveUser, Dashboard, AdminUsersAPI, AdminCampaignsAPI, AdminStatsAPI, AdminSponsorApprovalsAPI
from routes.campaign import CampaignAPI,CampaignDetailAPI
from routes.ad_request import AdRequestsAPI,SponsorAdRequestsAPI,InfluencerAdRequestsAPI  
from routes.influencer import AdRequests, SearchCampaigns, InfluencerProfileAPI,InfluencerProfilePictureUpload
from routes.sponsor import SponsorProfileResource, SponsorProfileCreateResource, SponsorProfileUpdateResource,AdRequestCreate,SearchInfluencers,CreateAdRequest
from flask_cors import CORS
from routes.influencer import InfluencerProfilePictureUpload






app = Flask(__name__)
CORS(app)
app.config.from_object(config['development']) 


celery_app = Celery('app', broker='redis://localhost:6379/0')
celery_app.conf.update(
    result_backend='redis://localhost:6379/1',  
                        
    timezone='Asia/Kolkata',
    worker_pool='eventlet',                   
                                
    task_default_queue='celery'                
                          
)


db.init_app(app)
jwt = JWTManager(app)
api = Api(app)

api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(ApproveUser, '/admin/approve_user/<int:user_id>')
api.add_resource(CampaignAPI, '/sponsor/campaigns')
api.add_resource(CampaignDetailAPI, '/sponsor/campaign/<int:campaign_id>')
api.add_resource(SponsorAdRequestsAPI, '/sponsor/ad_requests', '/sponsor/ad_requests/<int:ad_request_id>')


#influencers
api.add_resource(InfluencerProfilePictureUpload, '/influencer/profile/upload')
api.add_resource(InfluencerAdRequestsAPI,  '/influencer/ad_request', '/influencer/ad_requests/<int:ad_request_id>')
api.add_resource(AdRequestsAPI, '/influencer/send_ad_requests')
api.add_resource(SearchCampaigns, '/influencer/search_campaigns')
api.add_resource(InfluencerProfileAPI, '/influencer/profile')

#sponsors

api.add_resource(SearchInfluencers, '/sponsor/search_influencers')
api.add_resource(SponsorProfileCreateResource, '/profile/sponsor', methods=['POST'])  
api.add_resource(SponsorProfileResource, '/profiledetails/sponsor', methods=['GET'])  
api.add_resource(SponsorProfileUpdateResource, '/update/profile/sponsor', methods=['PUT'])

api.add_resource(CreateAdRequest,'/sponsor/create_ad_request/<int:influencer_id>')
api.add_resource(AdminCampaignsAPI, '/admin/campaigns', '/admin/campaigns/<int:campaign_id>')

#admin

api.add_resource(AdminUsersAPI, '/admin/users', '/admin/users/<int:user_id>')
api.add_resource(AdminStatsAPI, '/admin/stats')
api.add_resource(AdminSponsorApprovalsAPI, '/admin/sponsor_approvals', '/admin/sponsor_approvals/<int:sponsor_id>')



# @app.route('/test_celery')
# def test_celery():
    
#     celery_tasks.plus.delay(1,2)
#     return "triggered"

from flask_mail import Mail
mail = Mail()  

# @celery_app.task(name='send_daily_reminder')
# def send_daily_reminder():
#     with app.app_context():
#         influencers = User.query.filter_by(role='influencer').all()
#         for influencer in influencers:
#             pending_requests = AdRequest.query.filter_by(influencer_id=influencer.id, status='Pending').all()

#             if pending_requests:
#                 email_body = f"""
#                     <p>Hello {influencer.username},</p>
#                     <p>You have pending ad requests on the platform. Please log in to view and take action on them:</p>
#                     <p><a href="{url_for('influencer_dashboard', _external=True)}">Go to Dashboard</a></p> 
#                     <p>You can also check out public ad requests here:</p>
#                     <p><a href="{url_for('search_campaigns', _external=True)}">View Public Campaigns</a></p> 
#                 """

#                 msg = Message(
#                     subject="Daily Reminder: Pending Ad Requests",
#                     recipients=[influencer.email],
#                     html=email_body
#                 )
#                 mail.send(msg)

# celery_app.conf.beat_schedule = {
#     'send_daily_reminder': {
#         'task': 'send_daily_reminder',
#         'schedule': crontab(hour=16, minute=42)  
#     },
    
# }





with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
