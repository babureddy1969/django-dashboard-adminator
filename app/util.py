# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python


'''


echo "export SENDGRID_API_KEY='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'" > sendgrid.env
echo "sendgrid.env" >> .gitignore
source ./sendgrid.env
'''
from django.template.loader import render_to_string 
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
def sendmail():
    message = Mail(
        from_email='babureddy1969@gmail.com',
        to_emails='babureddy1969@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print()

def sendmail1(emails,sub,body):
    message = Mail(
        from_email='babureddy1969@gmail.com',
        to_emails=emails,
        subject=sub,
        html_content=body)
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def sendmail2(context):
    html_version = 'email/email.html'
    html_message = render_to_string(html_version, { 'context': context })
    print(html_message)
    subject = "Reg: Payment remittance {} USD {} Vendor : Smart Bee".format(context["clearing_date"],context["amount"])
    sendmail1(context["emails"],subject, html_message)
# sendmail2({"emails":["babureddy1969@gmail.com","babureddy@rocketmail.com"],"clearing_date":"2020-09-12","amount":1000,"supplier":"gm"})