from flask_restful import Resource
from flask import request
from models import db, AdRequest,Campaign
from flask_jwt_extended import jwt_required, get_jwt_identity
# from caching import cache
 
class AdRequestsAPI(Resource):
    def get(self):
        ad_requests = AdRequest.query.all()
        return [{"id": a.id, "status": a.status} for a in ad_requests], 200

    
    def post(self):
        try:
            data = request.get_json()
            print(f"Received data: {data}")  # Debugging log
            ad_request = AdRequest(
                campaign_id=data["campaign_id"],
                influencer_id=data["influencer_id"],
                requirements=data["requirements"],
                payment_amount=data["payment_amount"],
                  
                name=data.get("name"),
                status="Pending"
            )
            db.session.add(ad_request)
            db.session.commit()
            return {"message": "Ad request created successfully"}, 201
        except Exception as e:
            print(f"Error creating ad request: {e}")
            return {"message": "Failed to create ad request"}, 400
        
class SponsorAdRequestsAPI(Resource):
    @jwt_required()
    # @cache.cached(timeout=40)
    def get(self,ad_request_id=None):
        """
        Fetch all ad requests where the sponsor is involved
        """
        try:
          if ad_request_id is None:
            current_user = get_jwt_identity()
            user_id = current_user["id"]

            # Fetch campaigns created by the sponsor
            campaigns = Campaign.query.filter_by(sponsor_id=user_id).all()
            campaign_ids = [c.id for c in campaigns]

            # Fetch ad requests where the sponsor is involved
            ad_requests = AdRequest.query.filter(
                (AdRequest.campaign_id.in_(campaign_ids)) |
                (AdRequest.influencer_id == user_id)
            ).all()

            result = []
            for ad_request in ad_requests:
                result.append({
                    "id": ad_request.id,
                    "name": ad_request.name,
                    "campaign_name": ad_request.campaign.name,
                    "influencer_username": ad_request.influencer.username,
                    "status": ad_request.status,
                    "by_sponsor": ad_request.by_sponsor,
                })

            return result, 200
          else:
              ad_request = AdRequest.query.filter_by(id=ad_request_id).first()

              if not ad_request:
                    return {"message": "Ad request not found or unauthorized"}, 404

              return {
                    "id": ad_request.id,
                    "campaign_name": ad_request.campaign.name,
                    "status": ad_request.status,
                    "price": ad_request.payment_amount,
                    "negotiated_price": ad_request.negotiated_price,
                    "by_sponsor": ad_request.by_sponsor,
                    "name": ad_request.name,
                    "influencer_username": ad_request.influencer.username,
                    "requirements": ad_request.requirements
                }, 200

              

        except Exception as e:
            print(f"Error fetching sponsor ad requests: {e}")
            return {"message": "Failed to fetch ad requests"}, 500

    @jwt_required()
    def delete(self, ad_request_id):
        """
        Delete an ad request (only if it's pending and created by the sponsor)
        """
        try:
            current_user = get_jwt_identity()
            user_id = current_user["id"]

            ad_request = AdRequest.query.filter_by(id=ad_request_id).first()

            if not ad_request:
                return {"message": "Ad request not found"}, 404

            # Check if it's created by the sponsor and is still pending
            if not ad_request.by_sponsor or ad_request.status != "Pending":
                return {"message": "Cannot delete this ad request"}, 403

            db.session.delete(ad_request)
            db.session.commit()
            return {"message": "Ad request deleted successfully"}, 200

        except Exception as e:
            print(f"Error deleting ad request: {e}")
            return {"message": "Failed to delete ad request"}, 500

    @jwt_required()
    def post(self, ad_request_id):
        """
        Handle an ad request (accept/reject)
        """
        try:
            current_user = get_jwt_identity()
            user_id = current_user["id"]

            data = request.get_json()
            action = data.get("action")

            ad_request = AdRequest.query.filter_by(id=ad_request_id).first()

            if not ad_request:
                return {"message": "Ad request not found"}, 404

            # Only allow sponsors to handle received requests
            if ad_request.by_sponsor or ad_request.campaign.sponsor_id != user_id:
                return {"message": "Unauthorized"}, 403

            if action == "accept":
                ad_request.status = "Accepted"
            elif action == "reject":
                ad_request.status = "Rejected"
            else:
                return {"message": "Invalid action"}, 400

            db.session.commit()
            return {"message": f"Ad request {action}ed successfully"}, 200

        except Exception as e:
            print(f"Error handling ad request: {e}")
            return {"message": "Failed to handle ad request"}, 500
        

class InfluencerAdRequestsAPI(Resource):
    @jwt_required()
    def get(self, ad_request_id=None):
        """
        Fetch all ad requests for the influencer (both sent and received)
        or fetch a specific ad request by ID if ad_request_id is provided.
        """
        try:
            current_user = get_jwt_identity()
            influencer_id = current_user["id"]

            if ad_request_id is None:
                
                sent_requests = AdRequest.query.filter_by(influencer_id=influencer_id, by_sponsor=0).all()
                received_requests = AdRequest.query.filter_by(influencer_id=influencer_id, by_sponsor=1).all()

                ad_requests = []
                for ad_request in sent_requests:
                    ad_requests.append({
                        "id": ad_request.id,
                        "campaign_name": ad_request.campaign.name,
                        "status": ad_request.status,
                        "price": ad_request.payment_amount,
                        "negotiated_price": ad_request.negotiated_price,
                        "by_sponsor": ad_request.by_sponsor,
                        "name": ad_request.name,
                        "influencer_username": ad_request.influencer.username,
                        "type": "Sent"
                    })

                for ad_request in received_requests:
                    ad_requests.append({
                        "id": ad_request.id,
                        "campaign_name": ad_request.campaign.name,
                        "status": ad_request.status,
                        "price": ad_request.payment_amount,
                        "negotiated_price": ad_request.negotiated_price,
                        "by_sponsor": ad_request.by_sponsor,
                        "name": ad_request.name,
                        "influencer_username": ad_request.influencer.username,
                        "type": "Received"
                    })

                return ad_requests, 200

            else:
                # Fetch specific ad request if ad_request_id is provided
                ad_request = AdRequest.query.filter_by(id=ad_request_id, influencer_id=influencer_id).first()

                if not ad_request:
                    return {"message": "Ad request not found or unauthorized"}, 404

                return {
                    "id": ad_request.id,
                    "campaign_name": ad_request.campaign.name,
                    "status": ad_request.status,
                    "price": ad_request.payment_amount,
                    "negotiated_price": ad_request.negotiated_price,
                    "by_sponsor": ad_request.by_sponsor,
                    "name": ad_request.name,
                    "influencer_username": ad_request.influencer.username,
                    "requirements": ad_request.requirements
                }, 200

        except Exception as e:
            print(f"Error fetching influencer ad requests: {e}")
            return {"message": "Failed to fetch ad requests"}, 500

    @jwt_required()
    def post(self, ad_request_id):
        """
        Handle an ad request action (accept/reject/negotiation)
        """
        try:
            current_user = get_jwt_identity()
            influencer_id = current_user["id"]
            data = request.get_json()
            action = data.get("action")
            
            ad_request = AdRequest.query.filter_by(id=ad_request_id, influencer_id=influencer_id).first()

            if not ad_request:
                return {"message": "Ad request not found or unauthorized"}, 404

            if action == "accept":
                ad_request.status = "Accepted"
            elif action == "reject":
                ad_request.status = "Rejected"
            elif action == "negotiate":
                new_price = data.get("new_price")
                ad_request.negotiated_price = new_price
                ad_request.status = "Negotiation"
            else:
                return {"message": "Invalid action"}, 400

            db.session.commit()
            return {"message": f"Ad request {action}ed successfully"}, 200

        except Exception as e:
            print(f"Error handling ad request action: {e}")
            return {"message": "Failed to handle ad request"}, 500  
    
    @jwt_required()
    def put(self, ad_request_id):
        """
        Edit an ad request for the influencer (update details like price, status, etc.)
        """
        try:
            current_user = get_jwt_identity()
            influencer_id = current_user["id"]
            data = request.get_json()

            ad_request = AdRequest.query.filter_by(id=ad_request_id, influencer_id=influencer_id).first()
            if not ad_request:
                return {"message": "Ad request not found or unauthorized"}, 404

            # Update fields (Example: updating price, status, etc.)
            ad_request.payment_amount = data.get("price", ad_request.payment_amount)
            ad_request.status = data.get("status", ad_request.status)

            db.session.commit()
            return {"message": "Ad request updated successfully"}, 200

        except Exception as e:
            print(f"Error updating ad request: {e}")
            return {"message": "Failed to update ad request"}, 500

    @jwt_required()
    def delete(self, ad_request_id):
        """
        Delete an ad request (only if it's pending and created by the influencer)
        """
        try:
            current_user = get_jwt_identity()
            influencer_id = current_user["id"]

            ad_request = AdRequest.query.filter_by(id=ad_request_id, influencer_id=influencer_id).first()
            if not ad_request:
                return {"message": "Ad request not found or unauthorized"}, 404

            if ad_request.status != "Pending":
                return {"message": "Cannot delete this ad request"}, 403

            db.session.delete(ad_request)
            db.session.commit()
            return {"message": "Ad request deleted successfully"}, 200

        except Exception as e:
            print(f"Error deleting ad request: {e}")
            return {"message": "Failed to delete ad request"}, 500