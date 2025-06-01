from flask_mail import Mail, Message
from app import app

mail = Mail()

def send_email(to, subject, body, is_html=False):
    with app.app_context():  # Access the app context
        msg = Message(subject=subject, recipients=[to], html=body if is_html else None)
        mail.send(msg)