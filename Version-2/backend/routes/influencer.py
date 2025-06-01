from flask import request, jsonify
from flask_restful import Resource
from models import db, AdRequest, Campaign, User, InfluencerProfile
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from flask import url_for

class AdRequests(Resource):
    @jwt_required()

    def get(self):
        user_id = get_jwt_identity()["id"]
        ad_requests = AdRequest.query.filter_by(influencer_id=user_id, status="Pending").all()

        result = []
        for ad in ad_requests:
            result.append({
                "id": ad.id,
                "campaign_id": ad.campaign_id,
                "campaign_name": ad.campaign.name,  # Add campaign name
                "sponsor_name": ad.sponsor.company_name,  # Add sponsor name
                "requirements": ad.requirements,
                "payment_amount": ad.payment_amount,
                "status": ad.status
            })

        return jsonify(result)

class SearchCampaigns(Resource):
    @jwt_required()
    def get(self):
        # Get filter parameters from the request
        category = request.args.get("category")
        min_budget = request.args.get("min_budget", 0, type=float)
        max_budget = request.args.get("max_budget", float("inf"), type=float)

        # Fetch public campaigns matching the filters
        query = Campaign.query.filter_by(visibility="public")
        if category:
            query = query.filter(Campaign.goals.contains(category))
        if min_budget:
            query = query.filter(Campaign.budget >= min_budget)
        if max_budget:
            query = query.filter(Campaign.budget <= max_budget)

        campaigns = query.all()

        result = [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "budget": c.budget,
                "goals": c.goals
            } for c in campaigns
        ]

        return jsonify(result)

class InfluencerProfileAPI(Resource):
    
    @jwt_required()
    
    def get(self):
        user_id = get_jwt_identity()["id"]
        profile = InfluencerProfile.query.filter_by(user_id=user_id).first()

        if not profile:
            return {"message": "Profile not found"}, 404

        # Include the full path to the profile picture
        profile_picture_url = None
        if profile.profile_picture:
            profile_picture_url = url_for('static', filename=f'uploads/{profile.profile_picture}', _external=True)

        result = {
            "category": profile.category,
            "niche": profile.niche,
            "reach": profile.reach,
            "followers": profile.followers,
            "profile_picture": profile_picture_url,  # Include the URL
        }

        return result, 200

    @jwt_required()
    def put(self):
        # Get the current user's ID
        user_id = get_jwt_identity()["id"]

        # Fetch the influencer's profile
        profile = InfluencerProfile.query.filter_by(user_id=user_id).first()

        if not profile:
            return {"message": "Profile not found"}, 404

        # Update the profile details
        data = request.get_json()
        profile.category = data.get("category", profile.category)
        profile.niche = data.get("niche", profile.niche)
        profile.reach = data.get("reach", profile.reach)
        profile.followers = data.get("followers", profile.followers)

        db.session.commit()

        return {"message": "Profile updated successfully"}, 200
    

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, InfluencerProfile
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class InfluencerProfilePictureUpload(Resource):
    @jwt_required()
    def post(self):
        # Ensure upload directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Check for uploaded file
        if 'profile_picture' not in request.files:
            return {"message": "No file part"}, 400

        file = request.files['profile_picture']
        if file.filename == '':
            return {"message": "No selected file"}, 400

        if file and allowed_file(file.filename):
            # Save file
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Update influencer profile
            influencer_id = get_jwt_identity()["id"]
            influencer = InfluencerProfile.query.filter_by(user_id=influencer_id).first()
            if not influencer:
                return {"message": "Influencer profile not found"}, 404

            influencer.profile_picture = filename
            db.session.commit()

            return {"message": "Profile picture uploaded successfully", "profile_picture": filepath}, 200

        return {"message": "Invalid file type"}, 400
    


