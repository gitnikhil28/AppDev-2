from flask_restful import Resource
from models import db, User, InfluencerProfile, SponsorProfile
from flask import request, jsonify

class ApproveUser(Resource):
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        user.is_approved = True
        db.session.commit()
        return {"message": "User approved successfully"}, 200

class Dashboard(Resource):
    def get(self):
        active_users = User.query.filter_by(is_approved=True).count()
        total_campaigns = db.session.execute("SELECT COUNT(*) FROM campaigns").scalar()
        return {
            "active_users": active_users,
            "total_campaigns": total_campaigns
        }, 200

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User

from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, User

class AdminUsersAPI(Resource):
    @jwt_required()
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            result = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_flagged': user.is_flagged
            }
            if user.role == 'sponsor':
                sponsor_profile = SponsorProfile.query.filter_by(user_id=user.id).first()
                if sponsor_profile:
                    result['sponsor_details'] = {
                        'company_name': sponsor_profile.company_name,
                        'industry': sponsor_profile.industry,
                        'budget': sponsor_profile.budget
                    }
            elif user.role == 'influencer':
                influencer_profile = InfluencerProfile.query.filter_by(user_id=user.id).first()
                if influencer_profile:
                    result['influencer_details'] = {
                        'category': influencer_profile.category,
                        'niche': influencer_profile.niche,
                        'reach': influencer_profile.reach,
                        'followers': influencer_profile.followers
                    }
            return jsonify(result)
        else:
            users = User.query.filter(User.role != 'admin').all()
            result = [
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'is_flagged': user.is_flagged
                }
                for user in users
            ]
            return jsonify(result)

    @jwt_required()
    def put(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            user.is_flagged = not user.is_flagged
            db.session.commit()
            return {'message': f'User {user_id} flagged status updated'}, 200
        except Exception as e:
            return jsonify({'message': 'Failed to update flag status', 'error': str(e)}), 500

    @jwt_required()
    def delete(self, user_id):
        try:
            user = User.query.get_or_404(user_id)

            if user.sponsor_profile:
                db.session.delete(user.sponsor_profile)


            db.session.delete(user)
            db.session.commit()
            return {'message': f'User {user_id} deleted'}, 200
        except Exception as e:
            print("Error deleting user:", e)  # Add this for more detailed error logging
            return {'message': 'Failed to delete user', 'error': str(e)}, 500
        

from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, Campaign, User

class AdminCampaignsAPI(Resource):
    @jwt_required()
    def get(self, campaign_id=None):
        if campaign_id:
            campaign = Campaign.query.get_or_404(campaign_id)
            sponsor = User.query.get(campaign.sponsor_id)  # Fetch sponsor details
            result = {
                'id': campaign.id,
                'name': campaign.name,
                'sponsor_id': campaign.sponsor_id,
                'sponsor_name': sponsor.username if sponsor else 'Unknown',  # Include sponsor name
                'budget': campaign.budget,
                'is_flagged': campaign.is_flagged,
                'niche' : campaign.niche,
                'description' : campaign.description,
                'start_date' : campaign.start_date,
                'end_date' :  campaign.start_date,
                'visibility': campaign.visibility,
                'goals' : campaign.goals
            }
            return jsonify(result)
        else:
            campaigns = Campaign.query.all()
            result = []
            for campaign in campaigns:
                sponsor = User.query.get(campaign.sponsor_id)
                result.append({
                    'id': campaign.id,
                    'name': campaign.name,
                    'sponsor_id': campaign.sponsor_id,
                    'sponsor_name': sponsor.username if sponsor else 'Unknown',
                    'budget': campaign.budget,
                    'is_flagged': campaign.is_flagged,
                    'niche' : campaign.niche,
                    # ... other campaign details
                })
            return jsonify(result)

    @jwt_required()
    def put(self, campaign_id):
        try:
            campaign = Campaign.query.get_or_404(campaign_id)
            campaign.is_flagged = not campaign.is_flagged
            db.session.commit()
            return {'message': f'Campaign {campaign_id} flagged status updated'}, 200
        except Exception as e:
            return {'message': 'Failed to update flag status', 'error': str(e)}, 500
        

from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, User, Campaign, AdRequest
from sqlalchemy import func

class AdminStatsAPI(Resource):
    @jwt_required()
    def get(self):
        total_users = User.query.count()
        total_sponsors = User.query.filter_by(role='sponsor').count()
        total_influencers = User.query.filter_by(role='influencer').count()
        total_campaigns = Campaign.query.count()
        total_ad_requests = AdRequest.query.count()
        pending_ad_requests = AdRequest.query.filter_by(status='Pending').count()
        accepted_ad_requests = AdRequest.query.filter_by(status='Accepted').count()
        rejected_ad_requests = AdRequest.query.filter_by(status='Rejected').count()

        # Example: Campaigns per niche
        campaigns_per_niche = db.session.query(Campaign.niche, func.count(Campaign.id)).group_by(Campaign.niche).all()

        # Example: Ad requests per influencer
        ad_requests_per_influencer = db.session.query(User.username, func.count(AdRequest.id)).join(AdRequest, User.id == AdRequest.influencer_id).group_by(User.username).all()

        stats = {
            'total_users': total_users,
            'total_sponsors': total_sponsors,
            'total_influencers': total_influencers,
            'total_campaigns': total_campaigns,
            'total_ad_requests': total_ad_requests,
            'pending_ad_requests': pending_ad_requests,
            'accepted_ad_requests': accepted_ad_requests,
            'rejected_ad_requests': rejected_ad_requests,
            'campaigns_per_niche': [{'niche': niche, 'count': count} for niche, count in campaigns_per_niche],
            'ad_requests_per_influencer': [{'influencer': influencer, 'count': count} for influencer, count in ad_requests_per_influencer]
        }
        return jsonify(stats)


class AdminSponsorApprovalsAPI(Resource):
    @jwt_required()
    def get(self, sponsor_id=None):
        if sponsor_id:
            user = User.query.filter_by(id=sponsor_id, role='sponsor').first_or_404()
            sponsor_profile = SponsorProfile.query.filter_by(user_id=sponsor_id).first_or_404()
            result = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'company_name': sponsor_profile.company_name,
                'industry': sponsor_profile.industry,
                'budget': sponsor_profile.budget
            }
            return jsonify(result)
        else:
            sponsors = User.query.filter_by(role='sponsor', is_approved=False).all()  # Get unapproved sponsors
            result = []
            for sponsor in sponsors:
                sponsor_profile = SponsorProfile.query.filter_by(user_id=sponsor.id).first()
                if sponsor_profile:
                    result.append({
                        'id': sponsor.id,
                        'username': sponsor.username,
                        'email': sponsor.email,
                        'industry': sponsor_profile.industry
                    })
            return jsonify(result)

    @jwt_required()
    def put(self, sponsor_id):
        try:
            user = User.query.filter_by(id=sponsor_id, role='sponsor').first_or_404()
            user.is_approved = True
            db.session.commit()
            return {'message': f'Sponsor {sponsor_id} approved'}, 200
        except Exception as e:
            return {'message': 'Failed to approve sponsor', 'error': str(e)}, 500

    @jwt_required()
    def delete(self, sponsor_id):
        try:
            user = User.query.filter_by(id=sponsor_id, role='sponsor').first_or_404()
            sponsor_profile = SponsorProfile.query.filter_by(user_id=sponsor_id).first()
            if sponsor_profile:
                db.session.delete(sponsor_profile)
            db.session.delete(user)
            db.session.commit()
            return {'message': f'Sponsor {sponsor_id} deleted'}, 200
        except Exception as e:
            return jsonify({'message': 'Failed to delete sponsor', 'error': str(e)}), 500
