from flask import request,jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, SponsorProfile, User, AdRequest,InfluencerProfile,Campaign
from marshmallow import Schema, fields
from flask import url_for

class SponsorProfileSchema(Schema):
    company_name = fields.Str(required=True)
    industry = fields.Str(required=True)
    budget = fields.Float()

class SponsorProfileResource(Resource):
    @jwt_required()
    def get(self):
        """
        Get the current sponsor profile
        """
        # Get the current user's ID and role from JWT
        user_id = get_jwt_identity()["id"]
        user_role = get_jwt_identity()["role"]

        if user_role != "sponsor":
            return {"message": "You are not authorized to view sponsor profile"}, 403

        # Fetch the sponsor profile and user email
        profile = SponsorProfile.query.filter_by(user_id=user_id).first()
        user = User.query.filter_by(id=user_id).first()  # Fetch the user

        if not profile or not user:
            return {"message": "Sponsor profile not found"}, 404

        # Serialize the profile and include the user's email
        result = {
            "company_name": profile.company_name,
            "industry": profile.industry,
            "budget": profile.budget,
            "email": user.email  # Include email from the User table
        }

        return result, 200


class SponsorProfileCreateResource(Resource):
    @jwt_required()
    def post(self):
        """
        Create a new sponsor profile
        """
        # Get the current user's ID and role from JWT
        user_id = get_jwt_identity()["id"]
        user_role = get_jwt_identity()["role"]  # Assuming role is stored in JWT

        if user_role != "sponsor":
            return {"message": "You are not authorized to create a sponsor profile"}, 403

        # Check if the sponsor profile already exists
        existing_profile = SponsorProfile.query.filter_by(user_id=user_id).first()
        if existing_profile:
            return {"message": "Sponsor profile already exists"}, 400

        # Get the profile data from the request
        data = request.get_json()

        # Validate the data
        profile_schema = SponsorProfileSchema()
        try:
            profile_data = profile_schema.load(data)
        except Exception as e:
            return {"message": f"Error: {str(e)}"}, 400

        # Create new sponsor profile
        new_profile = SponsorProfile(
            user_id=user_id,
            company_name=profile_data["company_name"],
            industry=profile_data["industry"],
            budget=profile_data.get("budget")
        )

        db.session.add(new_profile)
        db.session.commit()

        return {"message": "Sponsor profile created successfully"}, 201


class SponsorProfileUpdateResource(Resource):
    @jwt_required()
    def put(self):
        """
        Update an existing sponsor profile
        """
        # Get the current user's ID and role from JWT
        user_id = get_jwt_identity()["id"]
        user_role = get_jwt_identity()["role"]  # Assuming role is stored in JWT

        if user_role != "sponsor":
            return {"message": "You are not authorized to update sponsor profile"}, 403

        # Fetch the sponsor profile
        profile = SponsorProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return {"message": "Sponsor profile not found"}, 404

        # Get the profile data from the request
        data = request.get_json()

        # Update the profile fields
        if "company_name" in data:
            profile.company_name = data["company_name"]
        if "industry" in data:
            profile.industry = data["industry"]
        if "budget" in data:
            profile.budget = data["budget"]

        db.session.commit()

        return {"message": "Sponsor profile updated successfully"}, 200
    
class AdRequestCreate(Resource):
    @jwt_required()
    def post(self):
        sponsor_id = get_jwt_identity()["id"]
        data = request.get_json()

        # Ensure the necessary data exists
        influencer_id = data.get("influencer_id")
        campaign_id = data.get("campaign_id")
        details = data.get("details")

        if not influencer_id or not campaign_id or not details:
            return {"message": "Missing required fields"}, 400

        # Create and add the ad request to the database
        ad_request = AdRequest(
            influencer_id=influencer_id,
            campaign_id=campaign_id,
            sponsor_id=sponsor_id,
            requirements=details,
            payment_amount=1000,  # Set a default or dynamic value for the payment
            status="Pending"  # Initial status
        )

        db.session.add(ad_request)
        db.session.commit()

        return {"message": "Ad request created successfully"}, 201

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, InfluencerProfile, User
from flask import url_for

NICHE_OPTIONS = [
    "Fashion & Beauty",
    "Lifestyle",
    "Travel",
    "Fitness & Health",
    "Gaming",
    "Food & Cooking",
    "Technology",
    "Finance",
    "Entertainment"
]

class SearchInfluencers(Resource):
    @jwt_required()
    def get(self):
        # Get filter parameters from the request
        niche = request.args.get("niche")
        min_reach = request.args.get("min_reach", 0, type=int)
        max_reach = request.args.get("max_reach", float("inf"), type=int)
        username = request.args.get("username")

        # Fetch influencers matching the filters
        query = db.session.query(InfluencerProfile, User).join(User, InfluencerProfile.user_id == User.id)
        if niche:
            query = query.filter(InfluencerProfile.niche.contains(niche))
        if min_reach:
            query = query.filter(InfluencerProfile.reach >= min_reach)
        if max_reach:
            query = query.filter(InfluencerProfile.reach <= max_reach)
        if username:
            query = query.filter(User.username.contains(username))

        influencers = query.all()

        result = []
        for influencer, user in influencers:
            result.append({
                "user_id": user.id,
                "username": user.username,
                "niche": influencer.niche,
                "reach": influencer.reach,
                "category": influencer.category,
                "followers": influencer.followers,
                "profile_picture": url_for('static', filename=f'uploads/{influencer.profile_picture}', _external=True)
            })

        return jsonify({"influencers": result, "niches": NICHE_OPTIONS})  # Include niches in the response
    

class CreateAdRequest(Resource):
    @jwt_required()
    def post(self, influencer_id):
        current_user_id = get_jwt_identity()

        try:
            sponsor = SponsorProfile.query.filter_by(user_id=current_user_id['id']).first()
            if not sponsor:
                return {'message': 'Sponsor not found'}, 404

            data = request.get_json()
            name = data.get('name')  
            campaign_id = data.get('campaign_id')
            messages = data.get('messages')
            requirements = data.get('requirements')
            payment_amount = float(data.get('payment_amount'))

            ad_request = AdRequest(
                name=name,  
                campaign_id=campaign_id,
                influencer_id=influencer_id,
                messages=messages,
                requirements=requirements,
                payment_amount=payment_amount,
                status='Pending',
                sponsor_id=sponsor.id ,
                by_sponsor=1 
            )
            db.session.add(ad_request)
            db.session.commit()

            return  {'message': 'Ad request created successfully'},200

        except Exception as e:
            print("Error creating ad request:", e)
            return {'message': 'Failed to create ad request', 'error': str(e)}, 505  
        

# @celery_app.task(name='export_campaign_data')
# def export_campaign_data(sponsor_id):
#     with app.app_context():
#         try:
#             campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()

#             csv_output = StringIO()
#             csv_writer = csv.writer(csv_output)

#             csv_writer.writerow(['Name', 'Description', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals'])

#             for campaign in campaigns:
#                 csv_writer.writerow([
#                     campaign.name,
#                     campaign.description,
#                     campaign.start_date,
#                     campaign.end_date,
#                     campaign.budget,
#                     campaign.visibility,
#                     campaign.goals
#                 ])

#             # Create the response object
#             response = make_response(csv_output.getvalue())
#             response.headers["Content-Disposition"] = "attachment; filename=campaign_data.csv"
#             response.headers["Content-type"] = "text/csv"

#             # Send an alert (example: print a message, or you can use another method to send an alert)
#             print(f"Campaign data exported for sponsor ID: {sponsor_id}")

#             return response  # Return the response object (optional)

#         except Exception as e:
#             print(f"Error exporting campaign data: {e}")
#             return jsonify({'message': 'Failed to export campaign data'}), 500

# class ExportCampaignData(Resource):
#     @jwt_required()
#     def post(self):
#         sponsor_id = get_jwt_identity()
#         task = export_campaign_data.delay(sponsor_id)
#         return jsonify({'message': 'Exporting campaign data in the background', 'task_id': task.id}), 202

