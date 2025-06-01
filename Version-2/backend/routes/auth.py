from flask import request, jsonify
from flask_restful import Resource
from models import db, User, SponsorProfile, InfluencerProfile
from flask_jwt_extended import create_access_token
from flask_bcrypt import generate_password_hash, check_password_hash

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")  # sponsor/influencer

        hashed_password = generate_password_hash(password).decode('utf-8') 

        if not all([username, email, password, role]):
            return {"message": "Missing required fields"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 400

        # Create a new User object
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Now add additional details based on the user's role
        if role == "sponsor":
            company_name = data.get("company_name")
            industry = data.get("industry")
            budget = data.get("budget")

            if not all([company_name, industry, budget]):
                return {"message": "Missing sponsor details"}, 400

            # Add sponsor-specific details to the database
            new_sponsor = SponsorProfile(user_id=new_user.id, company_name=company_name, industry=industry, budget=budget)
            db.session.add(new_sponsor)
            db.session.commit()

        elif role == "influencer":
            category = data.get("category")
            niche = data.get("niche")
            reach = data.get("reach")

            if not all([category, niche, reach]):
                return {"message": "Missing influencer details"}, 400

            # Add influencer-specific details to the database
            new_influencer = InfluencerProfile(user_id=new_user.id, category=category, niche=niche, reach=reach,followers=0)
            db.session.add(new_influencer)
            db.session.commit()

        return {"message": "User registered successfully"}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if user.role == 'sponsor' and not user.is_approved:
            return {"message": "You account is under review"}, 401
        
        if user and check_password_hash(user.password, password):
            # Generate JWT token including user role
            token = create_access_token(identity={"id": user.id, "role": user.role})
            return {"access_token": token, "role": user.role,"user_id": user.id}, 200
        
        return {"message": "Invalid credentials"}, 401