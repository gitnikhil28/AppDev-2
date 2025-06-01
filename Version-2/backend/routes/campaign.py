from flask_restful import Resource
from flask import request
from models import db, Campaign, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime


class CampaignAPI(Resource):
    @jwt_required()
    def get(self):
        """
        Fetch all campaigns created by the logged-in sponsor
        """
        try:
            sponsor_id = get_jwt_identity()["id"]
            print(f"Fetching campaigns for sponsor ID: {sponsor_id}")  # Debugging log

            sponsor = User.query.get(sponsor_id)
            if not sponsor:
                print("Sponsor not found!")  # Debugging log
                return {"message": "Sponsor not found"}, 404

            if sponsor.role != "sponsor":
                print(f"Invalid role: {sponsor.role}")  # Debugging log
                return {"message": "Unauthorized: Not a sponsor"}, 403

            campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
            print(f"Found campaigns: {len(campaigns)}")  # Debugging log

            return [
                {
                    "id": c.id,
                    "name": c.name,
                    "description": c.description,
                    "niche": c.niche,
                    "budget": c.budget,
                    "start_date": c.start_date.strftime('%Y-%m-%d'),
                    "end_date": c.end_date.strftime('%Y-%m-%d'),
                    "visibility": c.visibility,
                }
                for c in campaigns
            ], 200

        except Exception as e:
            print(f"Error fetching campaigns: {e}")  # Debugging log
            return {"message": "Failed to fetch campaigns"}, 500

    @jwt_required()
    def post(self):
        """
        Create a new campaign
        """
        data = request.get_json()
        sponsor_id = get_jwt_identity()["id"]
        sponsor = User.query.get(sponsor_id)

        if not sponsor or sponsor.role != "sponsor":
            return {"message": "Invalid sponsor"}, 403

        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()

        campaign = Campaign(
            name=data["name"],
            description=data["description"],
            start_date=start_date,
            end_date=end_date,
            budget=data["budget"],
            visibility=data["visibility"],
           
            niche=data.get("niche"),
            sponsor_id=sponsor_id,
        )
        db.session.add(campaign)
        db.session.commit()
        return {"message": "Campaign created successfully"}, 201


class CampaignDetailAPI(Resource):

    @jwt_required()
    def get(self, campaign_id):
        """
        Fetch details of a specific campaign
        """
        sponsor_id = get_jwt_identity()["id"]
        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=sponsor_id).first()

        if not campaign:
            return {"message": "Campaign not found or unauthorized"}, 404

        # Serialize the campaign details
        result = {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "start_date": campaign.start_date.strftime('%Y-%m-%d'),
            "end_date": campaign.end_date.strftime('%Y-%m-%d'),
            "budget": campaign.budget,
            "visibility": campaign.visibility,
            "goals": campaign.goals,
        }
        return result, 200


    @jwt_required()
    def delete(self, campaign_id):
        """
        Delete a specific campaign
        """
        sponsor_id = get_jwt_identity()["id"]
        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=sponsor_id).first()

        if not campaign:
            return {"message": "Campaign not found or unauthorized"}, 404

        db.session.delete(campaign)
        db.session.commit()
        return {"message": "Campaign deleted successfully"}, 200

    @jwt_required()
    def put(self, campaign_id):
        """
        Edit a specific campaign
        """
        sponsor_id = get_jwt_identity()["id"]
        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=sponsor_id).first()

        if not campaign:
            return {"message": "Campaign not found or unauthorized"}, 404

        data = request.get_json()

        campaign.name = data.get("name", campaign.name)
        campaign.description = data.get("description", campaign.description)
        campaign.start_date = datetime.strptime(
            data["start_date"], "%Y-%m-%d"
        ).date() if "start_date" in data else campaign.start_date
        campaign.end_date = datetime.strptime(
            data["end_date"], "%Y-%m-%d"
        ).date() if "end_date" in data else campaign.end_date
        campaign.budget = data.get("budget", campaign.budget)
        campaign.visibility = data.get("visibility", campaign.visibility)
        campaign.goals = data.get("goals", campaign.goals)

        db.session.commit()
        return {"message": "Campaign updated successfully"}, 200
    
class SearchCampaigns(Resource):
    @jwt_required()
    def get(self):
        """
        Search public campaigns for influencers
        """
        search = request.args.get("search", "").lower()
        niche = request.args.get("niche", "")

        query = Campaign.query.filter_by(visibility="public")
        if search:
            query = query.filter(Campaign.name.ilike(f"%{search}%"))
        if niche:
            query = query.filter(Campaign.goals.contains(niche))

        campaigns = query.all()

        return [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "start_date": c.start_date.strftime('%Y-%m-%d'),
                "end_date": c.end_date.strftime('%Y-%m-%d'),
                "sponsor_name": c.sponsor.username,
            }
            for c in campaigns
        ], 200