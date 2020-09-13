# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python


'''


echo "export SENDGRID_API_KEY='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'" > sendgrid.env
echo "sendgrid.env" >> .gitignore
source ./sendgrid.env
'''
from django.template.loader import render_to_string 
import base64
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
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
    subject = "Reg: Payment remittance for {} ${} {} Vendor : {}".format(context["clearing_date"],context["amount"],context["currency"],context["supplier"])
    sendmail1(context["emails"],subject, html_message)
# sendmail2({"emails":["babureddy1969@gmail.com","babureddy@rocketmail.com"],"clearing_date":"2020-09-12","amount":1000,"supplier":"gm","currency":"USD"})
def sendMailWithAttachment(context):
    # print(context)
    html_version = 'email/email.html'
    message = Mail(
        from_email='babureddy1969@gmail.com',
        to_emails=context['emails'],
        subject = "Reg: Payment remittance for {} ${} {} Vendor : {}".format(context["clearing_date"],context["amount"],context["currency"],context["supplier"]),
        html_content= render_to_string(html_version, { 'context': context })
    )
    with open(context['attachment'], 'rb') as f:
        data = f.read()
        f.close()
    print(data)
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('text/csv')
    attachment.file_name = FileName(context['attachment'])
    attachment.disposition = Disposition('attachment')
    attachment.content_id = ContentId('REMITTANCE')
    message.add_attachment(attachment)
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
# sendMailWithAttachment()