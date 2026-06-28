import resend
import secrets
from src.config import config
from jinja2 import Environment,FileSystemLoader,select_autoescape


resend.api_key = config.RESEND_API_KEY

env = Environment(
    loader=FileSystemLoader("src/emails/templetes"),
    autoescape = select_autoescape(["html","xml"])
)

user_email="user@gmail.com"

def send_otp_mail(email:str,templete:str,subject:str):
    otp = "".join(str(secrets.randbelow(10)) for _ in range(6))
    templete = env.get_template(templete)
    html = templete.render(user_email=user_email,
                           d1=otp[0],
                           d2=otp[1],
                           d3=otp[2],
                           d4=otp[3],
                           d5=otp[4],
                           d6=otp[5])
    params = {
        "from": "onboarding@resend.dev",
        "to": email,
        "subject":subject,
        "html":html
    }
    resend.Emails.send(params)
    return otp


def send_verificatin_mail(email:str):
    return send_otp_mail(email=email,templete='verify_new_user_email.html',subject="Verify Your Account")

def send_password_reset_mail(email:str):
    return send_otp_mail(email=email,templete='verify_new_user_email.html',subject="Password Reset")


